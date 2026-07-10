# Whisper POC (Python) - Simple Setup & Usage

This project is a proof of concept using OpenAI's Whisper model to transcribe audio files (like `.mp3`, `.m4a`, `.wav`, and `.mp4`) into text or subtitles.

## 1. Create the project folder
In Terminal:
```bash
mkdir whisper-poc
cd whisper-poc
```

## 2. Create a virtual environment
```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

```powershell
.\.venv\Scripts\Activate.ps1
```

## 3. Install the required libraries
Create `requirements.txt` with:

```text
openai>=1.30.0
python-dotenv>=1.0.1
imageio-ffmpeg>=0.5.1
```

Then install:

```bash
pip install -r requirements.txt
```

`imageio-ffmpeg` provides a bundled `ffmpeg` runtime, so large media files can be normalized and split automatically without a separate system install.

## 4. Add your OpenAI API key
Create a `.env` file in the project folder and add:

```text
OPENAI_API_KEY=sk-...your_key_here...
```

## 5. Add the transcription script
The script:
- Reads your `.env` file
- Loads the Whisper model (`whisper-1`)
- Sends small files directly to OpenAI
- Automatically normalizes and chunks oversized files before uploading
- Saves the result in `/outputs`

## 6. Run a transcription
```bash
python transcribe.py <your-audio-file> --language pt
```

For large video or audio files, use the same command shape:

```bash
python transcribe.py prompt_context_engineering_part1.mp4 --language pt
```

Output appears in:

```text
outputs/<your-audio-file-stem>.txt
```

## 7. Optional flags
| Option | What it does |
|---|---|
| `--language pt` | Forces Portuguese |
| `--prompt "..."` | Helps with names or terms |
| `--format srt` | Exports as subtitles |
| `--translate` | Translates to English |

Example:

```bash
python transcribe.py <your-audio-file> --language pt --format srt --prompt "Olá, este é um teste de transcrição com Whisper."
```
