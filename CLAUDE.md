# CLAUDE.md

## Project Summary

This repository is a Python CLI proof of concept for transcribing audio and video files with OpenAI.

- `transcribe.py` is the public entrypoint.
- `transcriber/` contains the implementation.
- Small files are uploaded directly.
- Large files are normalized, optionally chunked, transcribed, and merged.

## Architecture

### Entry Flow

- `transcribe.py`
  - Thin wrapper that calls `transcriber.cli.main()`.
- `transcriber/cli.py`
  - Parses CLI arguments.
  - Loads environment variables.
  - Validates inputs.
  - Chooses direct upload or large-file processing.
- `transcriber/openai_audio.py`
  - Builds the OpenAI client.
  - Builds shared request payloads.
  - Calls transcription or translation endpoints.
  - Normalizes SDK responses.
- `transcriber/media.py`
  - Resolves the bundled `ffmpeg` executable.
  - Normalizes media to mono `16 kHz` MP3.
  - Probes media duration.
  - Splits oversized normalized audio into upload-safe chunks.
- `transcriber/output.py`
  - Merges chunked `verbose_json` transcripts.
  - Offsets timestamps.
  - Renders `text`, `json`, `verbose_json`, `srt`, and `vtt` outputs.
  - Writes final output files.

### Large-File Strategy

The project uses `imageio-ffmpeg` only to locate a bundled `ffmpeg` executable.

- It does not use `imageio-ffmpeg` as a media-processing abstraction.
- Actual media work is still done by `ffmpeg` commands executed through `subprocess`.
- This avoids requiring every teammate to install `ffmpeg` globally.

## Common Commands

### PowerShell Setup

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Quick Verification

```powershell
python transcribe.py --help
```

### Example Runs

Small file:

```powershell
python transcribe.py <your-audio-file> --language pt
```

Large file:

```powershell
python transcribe.py prompt_context_engineering_part1.mp4 --language pt
```

Subtitle output:

```powershell
python transcribe.py <your-audio-file> --language pt --format srt
```

Outputs are written to `outputs/` by default.

## Repository Conventions

- Keep `transcribe.py` thin.
- Keep OpenAI request logic in `transcriber.openai_audio`.
- Keep ffmpeg and chunking logic in `transcriber.media`.
- Keep merge, render, and file output logic in `transcriber.output`.
- Preserve CLI behavior unless a requirement explicitly changes.
- Keep comments concise and technical.
- Update docs when architecture or workflow changes.

## Documentation Structure

This project treats documentation as part of the implementation, not as optional follow-up work.

### Documentation Roles

- `README.md`
  - Setup, environment, and usage instructions.
  - First stop for someone trying to run the project.
- `docs/specs/`
  - Feature specifications.
  - Source of truth for feature requirements, expected behavior, main flows, and feature-level architecture notes.
- `docs/adr/`
  - Architecture Decision Records.
  - Source of truth for important technical decisions, tradeoffs, dependency choices, and long-term consequences.
- `CLAUDE.md`
  - Contributor guide for engineers and AI agents.
  - Explains repo structure, working conventions, and when to update each documentation area.

### Why `docs/specs/` and `docs/adr/` Matter

These folders are important because they preserve project memory.

- `docs/specs/` explains what the feature is supposed to do.
- `docs/adr/` explains why the architecture works the way it does.
- Together, they help teammates and future agents understand both behavior and decision history.
- Code changes should not leave these folders behind when the design intent changes.

### Update Rules

Update a file in `docs/specs/` when:

- feature behavior changes
- user-facing flow changes
- output formats or processing rules change
- feature-level architecture description changes
- a new major feature is added

Create or update an ADR in `docs/adr/` when:

- a technical decision changes system structure
- a dependency decision changes
- the integration strategy changes
- a tradeoff with long-term impact is introduced
- a new architectural pattern or constraint is adopted

### Working Expectation

- Keep specs and ADRs aligned with the code.
- Do not let the implementation drift away from the documented intent.
- If a code change affects both behavior and architecture, update both the relevant spec and ADR.
- New major features should usually have a spec.
- Major design decisions should usually have an ADR.

## Documentation Map

- `README.md`
  - User setup and execution examples.
- `docs/specs/01-large-file-transcription-spec.md`
  - Feature requirements and current architecture description.
- `docs/adr/ADR-001-large-file-transcription-pipeline.md`
  - Architecture decision for bundled `ffmpeg` lookup and large-file preprocessing.

## Safe Change Guidance

- Do not replace `imageio-ffmpeg` casually; it is part of the current onboarding strategy.
- Do not move logic back into `transcribe.py`.
- If changing large-file behavior, update both the spec and ADR when the design intent changes.
- Prefer local verification such as imports, syntax checks, and `python transcribe.py --help` before live API runs.
