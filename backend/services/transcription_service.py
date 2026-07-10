from __future__ import annotations

import asyncio
import io
import tempfile
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from backend.config import get_settings
from transcription_from_source.transcriber import MAX_UPLOAD_BYTES
from transcription_from_source.transcriber.media import normalize_audio, resolve_ffmpeg_exe, split_audio
from transcription_from_source.transcriber.openai_audio import (
    build_client,
    build_common_request_args,
    serialize_result,
    transcribe_verbose_chunk,
)
from transcription_from_source.transcriber.output import merge_verbose_transcripts


class TranscriptionArgs:
    """Minimal args object matching what the migrated transcriber expects."""

    model = get_settings().whisper_model
    language = None
    prompt = None
    temperature = 0.0
    translate = False
    format = "verbose_json"


class TranscriptionService:
    """Wraps the migrated transcription module for FastAPI uploads."""

    def __init__(self):
        settings = get_settings()
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is required for transcription.")
        self.client = build_client(settings.openai_api_key)
        self.args = TranscriptionArgs()
        self.max_upload_bytes = settings.upload_max_bytes

    async def process(self, file: UploadFile) -> dict:
        file_bytes = await file.read()
        filename = file.filename or "upload"

        if len(file_bytes) > self.max_upload_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File exceeds the 200MB upload limit.",
            )

        if len(file_bytes) <= MAX_UPLOAD_BYTES:
            return await asyncio.to_thread(self._transcribe_small, file_bytes, filename)
        return await asyncio.to_thread(self._transcribe_large, file_bytes, filename)

    def _transcribe_small(self, file_bytes: bytes, filename: str) -> dict:
        with io.BytesIO(file_bytes) as handle:
            handle.name = filename
            common = build_common_request_args(self.args, handle, "verbose_json")
            result = self.client.audio.transcriptions.create(**common)

        payload = serialize_result(result)
        return {
            "content": payload.get("text", "") if isinstance(payload, dict) else str(payload),
            "duration_s": int(payload.get("duration", 0)) if isinstance(payload, dict) else 0,
            "filename": filename,
        }

    def _transcribe_large(self, file_bytes: bytes, filename: str) -> dict:
        ffmpeg_exe = resolve_ffmpeg_exe()
        safe_name = Path(filename).name or "upload.mp4"

        with tempfile.TemporaryDirectory(prefix="quiz-transcribe-") as tmp_dir:
            tmp_path = Path(tmp_dir)
            source_path = tmp_path / safe_name
            source_path.write_bytes(file_bytes)

            normalized_path = tmp_path / "normalized.mp3"
            normalize_audio(ffmpeg_exe, source_path, normalized_path)

            if normalized_path.stat().st_size <= MAX_UPLOAD_BYTES:
                merged = transcribe_verbose_chunk(self.client, normalized_path, self.args, 0.0)
            else:
                chunks = split_audio(ffmpeg_exe, normalized_path, tmp_path / "chunks")
                merged = merge_verbose_transcripts(
                    transcribe_verbose_chunk(self.client, chunk.path, self.args, chunk.offset_seconds)
                    for chunk in chunks
                )

        return {
            "content": merged.get("text", ""),
            "duration_s": int(merged.get("duration", 0)),
            "filename": filename,
        }