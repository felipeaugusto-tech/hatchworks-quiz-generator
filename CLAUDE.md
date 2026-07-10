# HatchWorks Quiz - CLAUDE.md

## Project Overview

Full-stack quiz generator: upload a video, transcribe it, generate questions, and complete an interactive quiz.

## Repository Structure

- `transcription_from_source/`
  - Migrated transcription CLI source.
  - Treat this as an internal dependency owned by the monorepo.
  - Wrap it from backend services instead of rewriting its core logic.
- `backend/`
  - FastAPI application, async database layer, API routes, services, specs, and ADRs.
- `frontend/`
  - Next.js App Router frontend with upload, quiz, and results screens.

## How to Run Locally

### Backend + Database

```bash
cp backend/.env.example backend/.env
# fill ANTHROPIC_API_KEY and OPENAI_API_KEY
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

## Documentation Rules

- Backend specs live in `backend/docs/specs/`.
- Backend ADRs live in `backend/docs/adr/`.
- Frontend specs live in `frontend/docs/specs/`.
- Frontend ADRs live in `frontend/docs/adr/`.
- The transcription module keeps its own docs under `transcription_from_source/docs/`.
- Update specs when behavior or flows change.
- Update ADRs when architecture, dependencies, or long-term tradeoffs change.

## Critical Rules

- NEVER change core logic inside `transcription_from_source/` unless the requirement is explicitly to evolve that module.
- NEVER save uploaded video or audio files permanently.
- ALWAYS validate Anthropic JSON responses and retry once on parse failure.
- ALWAYS keep backend database and external-service flows async.
- ALWAYS clean temporary files automatically through `TemporaryDirectory`.
- The frontend Dockerfile exists, but frontend is not part of `docker compose`.
- Prefer local verification such as imports, syntax checks, and API smoke tests before deployment.