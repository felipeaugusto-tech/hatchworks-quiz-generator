import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env (OPENAI_API_KEY)
load_dotenv()

def main():
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

    client = OpenAI(api_key=api_key)

    # Ensure output folder exists
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    audio_path = Path(args.audio).expanduser()
    if not audio_path.exists():
        raise SystemExit(f"File not found: {audio_path}")

    # Call Whisper
    with open(audio_path, "rb") as f:
        common = dict(
            model=args.model,
            file=f,
            response_format=args.format,
            temperature=args.temperature,
        )
        if args.prompt:
            common["prompt"] = args.prompt
        if args.language:
            common["language"] = args.language

        if args.translate:
            result = client.audio.translations.create(**common)  # to English
        else:
            result = client.audio.transcriptions.create(**common)

    # Map extension by chosen format
    ext = {
        "text": "txt",
        "json": "json",
        "verbose_json": "json",
        "srt": "srt",
        "vtt": "vtt",
    }.get(args.format, "txt")

    out_path = outdir / f"{audio_path.stem}.{ext}"

    # Write out (string or structured)
    if isinstance(result, str):
        out_path.write_text(result, encoding="utf-8")
    else:
        try:
            out_path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
        except Exception:
            out_path.write_text(str(result), encoding="utf-8")

    print(f"✅ Wrote {out_path.resolve()}")

if __name__ == "__main__":
    main()