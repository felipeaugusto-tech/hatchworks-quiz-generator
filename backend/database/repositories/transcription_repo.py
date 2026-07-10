from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models import Transcription


class TranscriptionRepository:
    """Handles persistence and lookup for transcription records."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, filename: str, content: str, duration_s: int | None) -> Transcription:
        transcription = Transcription(filename=filename, content=content, duration_s=duration_s)
        self.session.add(transcription)
        await self.session.flush()
        await self.session.refresh(transcription)
        return transcription

    async def get(self, transcription_id: UUID) -> Transcription | None:
        statement = select(Transcription).where(Transcription.id == transcription_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_recent(self) -> list[Transcription]:
        statement = select(Transcription).order_by(Transcription.created_at.desc())
        result = await self.session.execute(statement)
        return list(result.scalars().all())