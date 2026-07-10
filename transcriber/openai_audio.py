from pathlib import Path

from openai import OpenAI


def build_client(api_key: str) -> OpenAI:
    """Create the OpenAI client used by the transcription workflow."""
    return OpenAI(api_key=api_key)


def build_common_request_args(args, file_handle, response_format: str) -> dict:
    """Build shared request arguments for transcription and translation calls."""
    common = {
        "model": args.model,
        "file": file_handle,
        "response_format": response_format,
        "temperature": args.temperature,
    }
    if args.prompt:
        common["prompt"] = args.prompt
    if args.language:
        common["language"] = args.language
    return common


def transcribe_single_file(client: OpenAI, audio_path: Path, args):
    """Send a single small file directly to the appropriate OpenAI audio endpoint."""
    with open(audio_path, "rb") as handle:
        common = build_common_request_args(args, handle, args.format)
        if args.translate:
            return client.audio.translations.create(**common)
        return client.audio.transcriptions.create(**common)


def transcribe_verbose_chunk(client: OpenAI, audio_path: Path, args, offset_seconds: float) -> dict:
    """Transcribe one chunk as verbose JSON and attach its absolute time offset."""
    with open(audio_path, "rb") as handle:
        common = build_common_request_args(args, handle, "verbose_json")
        if args.translate:
            result = client.audio.translations.create(**common)
        else:
            result = client.audio.transcriptions.create(**common)

    payload = serialize_result(result)
    payload["offset_seconds"] = offset_seconds
    return payload


def serialize_result(result) -> object:
    """Normalize SDK responses into plain Python data structures when needed."""
    if isinstance(result, str):
        return result
    if hasattr(result, "model_dump"):
        return result.model_dump()
    if isinstance(result, dict):
        return result
    raise SystemExit("Unexpected transcription response type.")
