# ✅ Whisper POC (Python) — Simple Setup & Usage

This project is a **proof of concept** using OpenAI’s Whisper model to transcribe audio files (like `.mp3`, `.m4a`, `.wav`) into text or subtitles.

You set up everything step by step — here’s the recap.

---

## 🚀 1. Create the project folder
In Terminal:
```bash
mkdir whisper-poc
cd whisper-poc
```

---

## 🧩 2. Create a virtual environment
This keeps the project isolated from the rest of your system:
```bash
python3 -m venv .venv
```

Activate it:
<!-- Mac/Linux -->
```bash
source .venv/bin/activate
```

<!-- Windows -->
```bash
.\.venv\Scripts\Activate.ps1
```

You’ll know it worked if your terminal shows `(.venv)`.

---

## 📦 3. Install the required libraries
First, create the `requirements.txt` with:
```
openai>=1.30.0
python-dotenv>=1.0.1
```

Then install:
```bash
pip install -r requirements.txt
```

---

## 🔑 4. Add your OpenAI API key
Create a `.env` file in the project folder and add:
```
OPENAI_API_KEY=sk-...your_key_here...
```

This lets the script authenticate with OpenAI.

---

## 🧠 5. Add the transcription script
Create a file called `transcribe.py` with the code we added.  
This script:
- Reads your `.env` file  
- Loads the Whisper model (`whisper-1`)  
- Sends the audio to OpenAI  
- Saves the result in `/outputs`

---

## 🗣️ 6. Create a test audio (macOS shortcut)
```bash
say -v "Luciana" -o sample.aiff "Olá, este é um teste de transcrição com o Whisper."
afconvert -f m4af -d aac sample.aiff sample.m4a
```

---

## ▶️ 7. Run your first transcription
```bash
python transcribe.py sample.m4a --language pt
```

Output appears in:
```
outputs/sample.txt
```

✅ Example correct result:
```
Olá, este é um teste de transcrição com Whisper.
```

---

## 🎛 Optional flags you can use

| Option            | What it does                              |
|-------------------|-------------------------------------------|
| `--language pt`   | Forces Portuguese (no auto-detect risk)   |
| `--prompt "..."`  | Helps with names/terms                    |
| `--format srt`    | Exports as subtitle file                  |
| `--translate`     | Translates to English automatically       |

Example:
```bash
python transcribe.py sample.m4a --language pt --format srt --prompt "Olá, este é um teste de transcrição com Whisper."
```

---

## 📁 Project structure
```
whisper-poc/
├─ .venv/          ← virtual environment
├─ .env            ← your API key
├─ requirements.txt
├─ transcribe.py   ← main script
└─ outputs/        ← transcriptions created here
```

---

## ✅ What’s working now
✔ Python correctly installed  
✔ Virtual environment created  
✔ Dependencies installed  
✔ API key loaded from `.env`  
✔ First audio file created  
✔ Transcription works with correct text

---

## ✅ Next steps (optional)
You can ask for help to:
- Add batch transcription  
- Export SRT/VTT subtitles automatically  
- Translate to English  
- Wrap this as an API or simple UI  
- Integrate with FastAPI/Flask

Just say what you want next!
