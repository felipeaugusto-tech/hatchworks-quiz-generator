# HatchWorks Quiz

Full-stack quiz generator: upload a recording, transcribe it, generate multiple-choice questions, and complete the quiz in the browser.

## Repository Layout

- `transcription_from_source/`
  - Migrated transcription CLI module. This code is wrapped by the backend and should not be rewritten casually.
- `backend/`
  - FastAPI API, async SQLAlchemy models, Alembic migrations, repositories, and services.
- `frontend/`
  - Next.js 14 application for upload, quiz-taking, and results.
- `docker-compose.yml`
  - Local PostgreSQL + backend runtime.

## Python Startup Convention

This repository contains multiple Python projects. To avoid import-path issues, always run Python apps from the repository root using package-qualified module paths.

Examples:

- Backend:
  - `python -m uvicorn backend.main:app --reload`
- Transcription CLI:
  - `python transcription_from_source/transcribe.py --help`

Do not rely on running `uvicorn main:app` from inside `backend/`.

## Local Development

### Backend + Database

```bash
cp backend/.env.example backend/.env
# Fill OPENAI_API_KEY and ANTHROPIC_API_KEY

docker compose up --build
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Access

- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Documentation

- Backend feature and architecture docs live in `backend/docs/specs/` and `backend/docs/adr/`.
- Frontend feature and architecture docs live in `frontend/docs/specs/` and `frontend/docs/adr/`.
- The migrated transcription module keeps its own docs in `transcription_from_source/docs/`.