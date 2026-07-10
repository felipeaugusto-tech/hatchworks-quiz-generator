FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt /tmp/backend-requirements.txt
RUN pip install --no-cache-dir -r /tmp/backend-requirements.txt

COPY transcription_from_source/ /app/transcription_from_source/
COPY backend/ /app/backend/

EXPOSE 8000