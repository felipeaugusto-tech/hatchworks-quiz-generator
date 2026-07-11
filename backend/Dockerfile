FROM python:3.11-slim

WORKDIR /app

# This Dockerfile must be built from the monorepo root so Docker can access
# both `backend/` and `transcription_from_source/` in the same build context.
COPY backend/requirements.txt /tmp/backend-requirements.txt
RUN pip install --no-cache-dir -r /tmp/backend-requirements.txt

COPY transcription_from_source/ /app/transcription_from_source/
COPY backend/ /app/backend/

ENV PYTHONPATH=/app
WORKDIR /app/backend

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
