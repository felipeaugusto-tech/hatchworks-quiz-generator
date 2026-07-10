import argparse
import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv

from transcriber import API_UPLOAD_LIMIT_BYTES, EXTENSIONS, MAX_UPLOAD_BYTES
from transcriber.media import normalize_audio, resolve_ffmpeg_exe, split_audio
from transcriber.openai_audio import (
    build_client,
    serialize_result,
    transcribe_single_file,
    transcribe_verbose_chunk,
)
from transcriber.output import merge_verbose_transcripts, render_output, write_output


load_dotenv()


def main():
    """Parse CLI arguments and orchestrate the transcription workflow."""
    parser = argparse.ArgumentParser(description="Transcribe audio using OpenAI Whisper.")
    parser.add_argument("audio", help="Path to audio file (mp3, m4a, wav, etc.)")
    parser.add_argument("--format", default="text", help="text|json|verbose_json|srt|vtt (default: text)")
    parser.add_argument("--language", default=None, help="ISO code, e.g., 'pt' or 'en' (default: auto-detect)")
    parser.add_argument("--prompt", default=None, help="Hints for names/brands/terms")
    parser.add_argument("--temperature", type=float, default=0.0, help="0 = literal (default)")
    parser.add_argument("--model", default="whisper-1", help="Model name (default: whisper-1)")
    parser.add_argument("--translate", action="store_true", help="Translate to English instead of transcribing")
    parser.add_argument("--outdir", default="outputs", help="Where to save results (default: outputs)")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Missing OPENAI_API_KEY in environment or .env file.")

    client = build_client(api_key)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    audio_path = Path(args.audio).expanduser()
    if not audio_path.exists():
        raise SystemExit(f"File not found: {audio_path}")

    if args.format not in EXTENSIONS:
        supported = ", ".join(EXTENSIONS)
        raise SystemExit(f"Unsupported format '{args.format}'. Supported formats: {supported}")

    if audio_path.stat().st_size <= MAX_UPLOAD_BYTES:
        result = transcribe_single_file(client, audio_path, args)
        output_payload = serialize_result(result)
    else:
        output_payload = transcribe_large_file(client, audio_path, args)

    out_path = outdir / f"{audio_path.stem}.{EXTENSIONS[args.format]}"
    write_output(out_path, output_payload, args.format)
    print(f"Wrote {out_path.resolve()}")


def transcribe_large_file(client, audio_path: Path, args) -> object:
    """Normalize, optionally chunk, transcribe, and render oversized media files."""
    if audio_path.stat().st_size <= API_UPLOAD_LIMIT_BYTES:
        return serialize_result(transcribe_single_file(client, audio_path, args))

    ffmpeg_exe = resolve_ffmpeg_exe()

    with tempfile.TemporaryDirectory(prefix="transcribe-") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        normalized_path = temp_dir / "normalized.mp3"

        normalize_audio(ffmpeg_exe, audio_path, normalized_path)

        if normalized_path.stat().st_size <= MAX_UPLOAD_BYTES:
            merged = transcribe_verbose_chunk(client, normalized_path, args, 0.0)
        else:
            chunks = split_audio(ffmpeg_exe, normalized_path, temp_dir / "chunks")
            merged = merge_verbose_transcripts(
                transcribe_verbose_chunk(client, chunk.path, args, chunk.offset_seconds)
                for chunk in chunks
            )

        return render_output(merged, args.format)
