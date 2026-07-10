# ADR-001: Use bundled ffmpeg executable lookup for large-file preprocessing

## Status

Accepted

## Context

The transcription CLI originally uploaded the provided media file directly to the OpenAI audio API. That worked for smaller files but failed for larger recordings that exceeded the upload size limit.

To support large media files, the project needed a local preprocessing step that could:

- remove video from `.mp4` inputs
- normalize audio to a transcription-friendly format
- split normalized audio into upload-safe chunks when necessary

Those steps are standard `ffmpeg` operations.

The project also needed a way for teammates to run the tool without first installing `ffmpeg` globally and managing `PATH` manually on each machine.

The codebase also became harder to understand when CLI handling, OpenAI requests, media preprocessing, and output rendering all lived in one file.

## Decision

The project will keep local media preprocessing for large files and will use `imageio-ffmpeg` only to locate a bundled `ffmpeg` executable.

The implementation does not use `imageio-ffmpeg` as a media processing abstraction. Instead, it:

- calls `get_ffmpeg_exe()` to obtain the executable path
- runs normal `ffmpeg` commands through `subprocess`
- keeps orchestration logic in the Python application

The project will also separate responsibilities into a small package:

- `transcribe.py` remains a thin entrypoint
- `transcriber.cli` handles CLI orchestration
- `transcriber.openai_audio` handles OpenAI requests
- `transcriber.media` handles ffmpeg resolution, normalization, and chunking
- `transcriber.output` handles transcript merging and final rendering

This keeps the dependency decision narrow and the code structure easier to explain:

- `imageio-ffmpeg` handles executable distribution
- `ffmpeg` handles media work
- the `transcriber` package handles workflow control

## Alternatives Considered

### 1. Require system `ffmpeg` on `PATH`

Pros:
- fewer Python dependencies
- more obvious architecture for engineers already familiar with ffmpeg

Cons:
- adds setup friction for teammates
- introduces machine-specific PATH issues
- makes onboarding less predictable

### 2. Remove automatic preprocessing and require manual preparation

Pros:
- simplest code path
- avoids local media-processing logic in the project

Cons:
- worse user experience
- makes the CLI inconsistent between small and large files
- pushes operational knowledge onto every user

### 3. Drop large-file support entirely

Pros:
- smallest implementation surface

Cons:
- does not solve the observed `413` failure
- makes the tool unsuitable for long recordings and video sources

## Consequences

- Teammates can run large-file transcription without separately installing `ffmpeg`.
- The dependency list grows by one package.
- The architecture is easier to read because the main responsibilities are now separated into focused modules.
- The project still depends on direct ffmpeg subprocess execution and media duration parsing.
- The dependency choice should still be revisited in the future if the team prefers a system-level ffmpeg requirement.
