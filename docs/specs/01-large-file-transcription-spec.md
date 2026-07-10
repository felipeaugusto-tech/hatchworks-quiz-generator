# Large-File Transcription Support - Spec

> **Status:** Draft
> **Author:** @codex
> **Created:** 2026-07-09
> **Last updated:** 2026-07-10
> **Related ADRs:** [ADR-001](../adr/ADR-001-large-file-transcription-pipeline.md)

---

## 1. Overview

This feature allows the transcription CLI to handle large audio and video files without asking the user to manually convert or split them first. The user-facing command stays the same, but the implementation is now organized into a small `transcriber/` package so each responsibility is easier to understand and maintain.

---

## 2. Goals

- Support large media files that would otherwise fail with the OpenAI upload size limit.
- Keep the command-line interface unchanged for users.
- Make the implementation understandable enough to share with teammates.
- Preserve output support for plain text, JSON, and subtitle formats.
- Separate CLI orchestration, OpenAI calls, media processing, and output rendering into clear modules.

## 3. Non-Goals

- Changing CLI arguments or runtime behavior.
- Replacing `imageio-ffmpeg` in this iteration.
- Adding a GUI, background processing, or a service layer.
- Adding new transcription features such as speaker diarization or summarization.

---

## 4. Background & Context

The original script uploaded the provided file directly to the OpenAI audio API. That works for smaller files, but large recordings can exceed the upload limit and fail with HTTP `413`. To make the CLI usable for longer recordings and video files, the implementation was extended to preprocess large inputs locally before uploading them.

That large-file flow is still the same, but the code is no longer concentrated in a single monolithic script. The current architecture keeps `transcribe.py` as a thin entrypoint and moves the logic into focused modules inside `transcriber/`.

---

## 5. Functional Requirements

Use MUST, SHOULD, and MAY as defined by RFC 2119.

### 5.1 CLI and Validation

| ID     | Requirement | Priority |
| ------ | ----------- | -------- |
| REQ-01 | The system MUST accept the existing positional `audio` argument and the flags `--format`, `--language`, `--prompt`, `--temperature`, `--model`, `--translate`, and `--outdir`. | P0 |
| REQ-02 | The system MUST load `OPENAI_API_KEY` from the environment or `.env` file before attempting transcription. | P0 |
| REQ-03 | The system MUST fail clearly when the input file does not exist. | P0 |
| REQ-04 | The system MUST reject unsupported output formats with a clear validation message. | P0 |

### 5.2 Direct Transcription Path

| ID     | Requirement | Priority |
| ------ | ----------- | -------- |
| REQ-05 | The system MUST upload files at or below the safe working upload threshold directly to the OpenAI audio endpoint. | P0 |
| REQ-06 | The system MUST call the translation endpoint when `--translate` is enabled and the transcription endpoint otherwise. | P0 |
| REQ-07 | The system MUST request the user-selected response format for direct uploads. | P1 |

### 5.3 Large-File Preprocessing Path

| ID     | Requirement | Priority |
| ------ | ----------- | -------- |
| REQ-08 | The system MUST detect when an input is too large for the direct upload path. | P0 |
| REQ-09 | The system MUST preprocess oversized media locally before upload. | P0 |
| REQ-10 | The system MUST remove video, convert audio to mono, resample to `16 kHz`, and encode to a low-bitrate MP3 during normalization. | P0 |
| REQ-11 | If the normalized file still exceeds the safe upload threshold, the system MUST split it into sequential chunks. | P0 |
| REQ-12 | The system MUST preserve chunk order and calculate chunk offsets for later transcript merging. | P0 |

### 5.4 Transcript Merging and Output Rendering

| ID     | Requirement | Priority |
| ------ | ----------- | -------- |
| REQ-13 | The system MUST use `verbose_json` as the internal format for chunked transcription so timestamps can be merged deterministically. | P0 |
| REQ-14 | The system MUST shift timestamps by chunk offset before merging chunk results. | P0 |
| REQ-15 | The system MUST render the final output as `text`, `json`, `verbose_json`, `srt`, or `vtt` according to the requested output format. | P0 |
| REQ-16 | The system MUST write the final result to the selected output directory using the source file stem and the format-based extension. | P0 |

### 5.5 Failure Handling

| ID     | Requirement | Priority |
| ------ | ----------- | -------- |
| REQ-17 | The system MUST fail with a targeted error if local media preprocessing cannot start or complete. | P0 |
| REQ-18 | The system MUST fail with a targeted error if chunk sizing cannot be calculated. | P0 |
| REQ-19 | The system MUST fail with a targeted error if chunking still cannot reduce uploads below the safe threshold. | P0 |
| REQ-20 | The system SHOULD replace raw size-limit failures with clearer local-processing errors where possible. | P1 |

---

## 6. Non-Functional Requirements

| Category | Requirement |
| -------- | ----------- |
| Portability | The feature SHOULD work on teammate machines without requiring a separate global `ffmpeg` installation. |
| Maintainability | The implementation SHOULD keep separate modules for CLI orchestration, OpenAI calls, media processing, and output rendering. |
| Reliability | Temporary files MUST be created in a temporary working directory and cleaned up automatically. |
| Observability | The script SHOULD print a clear output path on success and actionable errors on failure. |
| Simplicity | The user-facing CLI SHOULD remain stable even if internal processing becomes more complex. |

---

## 7. Why `imageio-ffmpeg` Is Used

The project uses `imageio-ffmpeg` for one reason: it provides a local `ffmpeg` executable that Python can locate reliably.

The application does **not** use `imageio-ffmpeg` as a media-processing API. Instead, it calls:

- `get_ffmpeg_exe()` to find the bundled executable path
- `subprocess.run(...)` to execute normal `ffmpeg` commands

This choice avoids asking every teammate to install `ffmpeg` globally and configure `PATH` correctly before the script can process large files.

In practical terms:

- `imageio-ffmpeg` solves executable distribution
- `ffmpeg` still performs the real normalization, duration probing, and chunking
- the `transcriber` package remains responsible for orchestration

---

## 8. User Stories / Scenarios

```text
As a CLI user,
I want to transcribe a large audio or video file with the same command I use for small files,
So that I do not need to manually preprocess media before using the tool.
```

```text
As a teammate reviewing the project,
I want the large-file path and its dependencies to be explained clearly,
So that I can understand why the tool uses ffmpeg-related tooling.
```

### Acceptance Criteria

- [ ] Given a small supported media file, when the user runs the CLI, then the file is uploaded directly and the output is written successfully.
- [ ] Given an oversized media file, when the user runs the same command, then the tool preprocesses the file locally before upload.
- [ ] Given a normalized file that is still too large, when chunking runs, then chunks are transcribed in order and merged into one final output.
- [ ] Given subtitle output, when chunked transcription occurs, then the resulting timestamps are offset correctly.
- [ ] Given a teammate reading the docs, when they review the dependency explanation, then they can understand why `imageio-ffmpeg` is present.

---

## 9. Technical Design

### 9.1 High-Level Flow

```text
[transcribe.py]
    -> [transcriber.cli]
        -> [argument parsing and env loading]
        -> [input validation]
        -> [size check]
            -> small file: [transcriber.openai_audio]
            -> large file: [transcriber.media]
                           -> [normalize media]
                           -> [optionally split into chunks]
                           -> [transcriber.openai_audio transcribes chunks]
                           -> [transcriber.output merges and renders]
        -> [write output file]
```

### 9.2 Current Module Responsibilities

- `transcribe.py`
  - thin CLI entrypoint only
- `transcriber.cli`
  - argument parsing, env loading, path validation, top-level orchestration
- `transcriber.openai_audio`
  - OpenAI client construction, request building, direct transcription, chunk transcription, response serialization
- `transcriber.media`
  - bundled ffmpeg lookup, normalization, duration probing, chunk splitting
- `transcriber.output`
  - transcript merging, timestamp shifting, subtitle rendering, final file writing

### 9.3 Current Internal Structures

```ts
interface Chunk {
  path: string;
  offset_seconds: number;
}

interface MergedTranscript {
  text: string;
  language: string | null;
  duration: number;
  segments: Array<Record<string, unknown>>;
  words: Array<Record<string, unknown>>;
}
```

---

## 10. Error Handling

| Scenario | Behavior |
| -------- | -------- |
| Missing API key | Exit before any API call with a configuration error. |
| Missing input file | Exit with a file-not-found error. |
| Unsupported format | Exit with a validation error listing supported formats. |
| ffmpeg executable cannot be resolved | Exit with a preprocessing dependency error. |
| Media duration cannot be determined | Exit with a chunking preparation error. |
| Chunking still cannot reduce size enough | Exit with an actionable preprocessing error. |
| Upstream API failure | Surface the SDK error. |

---

## 11. Open Questions

| # | Question | Owner | Status |
| --- | -------- | ----- | ------ |
| 1 | Should the project eventually replace bundled ffmpeg with a system dependency? | @team | Open |
| 2 | Should future versions add retry handling for failed chunk uploads? | @team | Open |

---

## 12. Out of Scope / Future Work

- Change CLI behavior or supported options in this iteration.
- Replace `imageio-ffmpeg` in this iteration.
- Add progress reporting or background execution.
- Add batch transcription, caching, or retry workflows.
- Add richer transcript semantics such as speaker labeling.

---

## 13. References

- [Project README](../../README.md)
- [CLI entrypoint](../../transcribe.py)
- [Package directory](../../transcriber)
- [ADR-001](../adr/ADR-001-large-file-transcription-pipeline.md)
