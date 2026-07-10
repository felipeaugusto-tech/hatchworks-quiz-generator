# Transcription Feature Spec

## Objective
Accept a video or audio upload, transcribe it with the OpenAI Whisper API,
save the transcription to PostgreSQL, and return a transcription identifier.

## Contract
POST /transcribe
multipart/form-data: file (video/audio, max 200MB)

Response:
{ "transcription_id": "uuid", "duration_s": 120, "preview": "..." }

## Business Rules
- Files <= 24MB: process in memory, no temp files.
- Files > 24MB: use the `transcription_from_source` ffmpeg pipeline.
- Video files (.mp4): normalize to mono MP3 before transcription.
- Save transcription text and duration to the database.
- Do not store media files permanently.

## Edge Cases
- File > 200MB -> 413 before transcription starts.
- Whisper API error -> 500 and no partial database save.
- Missing OPENAI_API_KEY -> startup failure.