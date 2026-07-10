import math
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from imageio_ffmpeg import get_ffmpeg_exe

from . import (
    CHUNK_SAFETY_FACTOR,
    MAX_UPLOAD_BYTES,
    MIN_CHUNK_SECONDS,
    NORMALIZED_AUDIO_BITRATE,
    NORMALIZED_AUDIO_RATE,
)


@dataclass
class Chunk:
    """Represents one normalized audio chunk and its timeline offset."""

    path: Path
    offset_seconds: float


def resolve_ffmpeg_exe() -> str:
    """Resolve the bundled ffmpeg executable used for local media processing."""
    try:
        return get_ffmpeg_exe()
    except Exception as exc:
        raise SystemExit(
            "Large-file transcription requires the bundled ffmpeg runtime. "
            "Install dependencies again so imageio-ffmpeg is available."
        ) from exc


def normalize_audio(ffmpeg_exe: str, source_path: Path, target_path: Path) -> None:
    """Convert source media into a mono, speech-friendly MP3 for transcription."""
    command = [
        ffmpeg_exe,
        "-y",
        "-i",
        str(source_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        str(NORMALIZED_AUDIO_RATE),
        "-b:a",
        NORMALIZED_AUDIO_BITRATE,
        str(target_path),
    ]
    run_ffmpeg(command, f"Failed to normalize audio from {source_path.name}")


def split_audio(ffmpeg_exe: str, normalized_path: Path, chunks_dir: Path) -> list[Chunk]:
    """Split normalized audio into upload-safe chunks based on size and duration."""
    chunks_dir.mkdir(parents=True, exist_ok=True)

    duration_seconds = get_media_duration_seconds(ffmpeg_exe, normalized_path)
    if duration_seconds <= 0:
        raise SystemExit("Unable to determine normalized audio duration for chunking.")

    bytes_per_second = normalized_path.stat().st_size / duration_seconds
    target_chunk_seconds = max(
        MIN_CHUNK_SECONDS,
        int((MAX_UPLOAD_BYTES * CHUNK_SAFETY_FACTOR) / bytes_per_second),
    )

    while True:
        for existing_chunk in chunks_dir.glob("chunk_*.mp3"):
            existing_chunk.unlink()

        output_pattern = chunks_dir / "chunk_%03d.mp3"
        command = [
            ffmpeg_exe,
            "-y",
            "-i",
            str(normalized_path),
            "-f",
            "segment",
            "-segment_time",
            str(target_chunk_seconds),
            "-c",
            "copy",
            str(output_pattern),
        ]
        run_ffmpeg(command, "Failed to split normalized audio into chunks.")

        chunk_paths = sorted(chunks_dir.glob("chunk_*.mp3"))
        if not chunk_paths:
            raise SystemExit("Chunking produced no output files.")

        if all(chunk_path.stat().st_size <= MAX_UPLOAD_BYTES for chunk_path in chunk_paths):
            break

        if target_chunk_seconds <= MIN_CHUNK_SECONDS:
            raise SystemExit(
                "Chunked audio still exceeds the upload limit after normalization. "
                "Try lowering the source audio bitrate manually."
            )

        target_chunk_seconds = max(MIN_CHUNK_SECONDS, math.floor(target_chunk_seconds / 2))

    chunks: list[Chunk] = []
    elapsed_seconds = 0.0
    for chunk_path in chunk_paths:
        chunks.append(Chunk(path=chunk_path, offset_seconds=elapsed_seconds))
        chunk_duration = get_media_duration_seconds(ffmpeg_exe, chunk_path)
        elapsed_seconds += chunk_duration or target_chunk_seconds
    return chunks


def get_media_duration_seconds(ffmpeg_exe: str, media_path: Path) -> float:
    """Read media duration by parsing ffmpeg metadata output."""
    command = [ffmpeg_exe, "-i", str(media_path)]
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    output = f"{completed.stdout}\n{completed.stderr}"
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", output)
    if not match:
        return 0.0

    hours = int(match.group(1))
    minutes = int(match.group(2))
    seconds = float(match.group(3))
    return hours * 3600 + minutes * 60 + seconds


def run_ffmpeg(command: list[str], error_message: str) -> None:
    """Run an ffmpeg command and raise a targeted error on failure."""
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        details = completed.stderr.strip() or completed.stdout.strip() or "No ffmpeg output."
        raise SystemExit(f"{error_message}\n{details}")
