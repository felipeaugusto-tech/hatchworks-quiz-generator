import json
from pathlib import Path


def merge_verbose_transcripts(results) -> dict:
    """Merge chunked verbose transcription payloads into one combined transcript."""
    merged = {
        "text": "",
        "language": None,
        "duration": 0.0,
        "segments": [],
        "words": [],
    }
    next_segment_id = 0
    text_parts = []

    for result in results:
        offset = float(result.get("offset_seconds", 0.0))
        if not merged["language"]:
            merged["language"] = result.get("language")

        text = (result.get("text") or "").strip()
        if text:
            text_parts.append(text)

        merged["duration"] = max(
            merged["duration"],
            offset + float(result.get("duration") or 0.0),
        )

        for segment in result.get("segments") or []:
            shifted_segment = dict(segment)
            shifted_segment["id"] = next_segment_id
            next_segment_id += 1
            shift_timestamp_fields(shifted_segment, offset, ("start", "end", "seek"))

            if shifted_segment.get("words"):
                shifted_words = []
                for word in shifted_segment["words"]:
                    shifted_word = dict(word)
                    shift_timestamp_fields(shifted_word, offset, ("start", "end"))
                    shifted_words.append(shifted_word)
                shifted_segment["words"] = shifted_words

            merged["segments"].append(shifted_segment)

        for word in result.get("words") or []:
            shifted_word = dict(word)
            shift_timestamp_fields(shifted_word, offset, ("start", "end"))
            merged["words"].append(shifted_word)

    merged["text"] = "\n\n".join(text_parts).strip()
    return merged


def shift_timestamp_fields(payload: dict, offset_seconds: float, keys: tuple[str, ...]) -> None:
    """Offset selected timestamp fields in-place by the given chunk start time."""
    for key in keys:
        if key in payload and payload[key] is not None:
            payload[key] = round(float(payload[key]) + offset_seconds, 3)


def render_output(merged: dict, output_format: str):
    """Render a merged transcript into the user-requested output format."""
    if output_format == "text":
        return merged["text"]
    if output_format == "srt":
        return render_srt(merged)
    if output_format == "vtt":
        return render_vtt(merged)
    return merged


def render_srt(merged: dict) -> str:
    """Render merged transcript segments as an SRT subtitle document."""
    entries = []
    for index, segment in enumerate(select_caption_segments(merged), start=1):
        entries.append(
            "\n".join(
                [
                    str(index),
                    f"{format_timestamp(segment['start'], srt=True)} --> {format_timestamp(segment['end'], srt=True)}",
                    segment["text"].strip(),
                ]
            )
        )
    return "\n\n".join(entries).strip() + "\n"


def render_vtt(merged: dict) -> str:
    """Render merged transcript segments as a VTT subtitle document."""
    entries = ["WEBVTT"]
    for segment in select_caption_segments(merged):
        entries.append(
            "\n".join(
                [
                    "",
                    f"{format_timestamp(segment['start'], srt=False)} --> {format_timestamp(segment['end'], srt=False)}",
                    segment["text"].strip(),
                ]
            )
        )
    return "\n".join(entries).strip() + "\n"


def select_caption_segments(merged: dict) -> list[dict]:
    """Extract caption-ready segments from merged transcript data."""
    segments = merged.get("segments") or []
    if segments:
        return [
            {
                "start": float(segment.get("start") or 0.0),
                "end": float(segment.get("end") or 0.0),
                "text": (segment.get("text") or "").strip(),
            }
            for segment in segments
            if (segment.get("text") or "").strip()
        ]

    text = (merged.get("text") or "").strip()
    if not text:
        return []

    return [{"start": 0.0, "end": float(merged.get("duration") or 0.0), "text": text}]


def format_timestamp(total_seconds: float, *, srt: bool) -> str:
    """Format seconds into SRT or VTT timestamp notation."""
    total_milliseconds = max(0, round(total_seconds * 1000))
    hours, remainder = divmod(total_milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, milliseconds = divmod(remainder, 1_000)
    separator = "," if srt else "."
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}{separator}{milliseconds:03d}"


def write_output(out_path: Path, payload, output_format: str) -> None:
    """Write rendered output to disk using text or JSON serialization as needed."""
    if output_format in {"text", "srt", "vtt"}:
        out_path.write_text(str(payload), encoding="utf-8")
    else:
        out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
