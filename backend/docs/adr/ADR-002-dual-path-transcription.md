# ADR 002 - Dual-Path Transcription (in-memory vs disk)

Date: 2026-07-10 | Status: Accepted

## Context
The migrated `transcription_from_source` module already uses a dual-path
strategy based on file size and relies on a bundled ffmpeg executable resolved
through `imageio-ffmpeg`.

## Decision
Maintain the existing strategy:

- Small files (<=24MB): read bytes in memory and send directly to the OpenAI SDK.
- Large files (>24MB): write to a temporary directory, normalize through ffmpeg,
  optionally split into chunks, transcribe each chunk, and merge the results.

The backend wraps this behavior and never rewrites the underlying logic.

## Consequences
+ No permanent media storage.
+ Large-file support is preserved without reimplementation.
+ The backend receives a simple normalized dict from the wrapper service.
- Large files still require temporary disk writes.