from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.connection import get_db_session
from backend.database.repositories.transcription_repo import TranscriptionRepository
from backend.schemas.schemas import TranscribeResponse, TranscriptionListItem
from backend.services.transcription_service import TranscriptionService

router = APIRouter(tags=["transcription"])


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_file(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db_session),
) -> TranscribeResponse:
    service = TranscriptionService()
    payload = await service.process(file)

    repo = TranscriptionRepository(session)
    transcription = await repo.create(
        filename=payload["filename"],
        content=payload["content"],
        duration_s=payload["duration_s"],
    )
    await session.commit()

    return TranscribeResponse(
        transcription_id=transcription.id,
        duration_s=payload["duration_s"],
        preview=payload["content"][:200],
    )


@router.get("/transcriptions", response_model=list[TranscriptionListItem])
async def list_transcriptions(session: AsyncSession = Depends(get_db_session)) -> list[TranscriptionListItem]:
    repo = TranscriptionRepository(session)
    rows = await repo.list_recent()
    return [
        TranscriptionListItem(
            id=row.id,
            filename=row.filename,
            duration_s=row.duration_s,
            created_at=row.created_at,
            preview=row.content[:200],
        )
        for row in rows
    ]