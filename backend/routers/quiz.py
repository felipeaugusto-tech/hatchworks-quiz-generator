from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.connection import get_db_session
from backend.database.repositories.quiz_repo import QuizRepository
from backend.database.repositories.transcription_repo import TranscriptionRepository
from backend.schemas.schemas import GenerateQuizRequest, QuizListItem, QuizOut
from backend.services.quiz_service import QuizGenerationError, QuizService

router = APIRouter(tags=["quiz"])


@router.post("/quiz/generate", response_model=QuizOut)
async def generate_quiz(
    request: GenerateQuizRequest,
    session: AsyncSession = Depends(get_db_session),
) -> QuizOut:
    transcription_repo = TranscriptionRepository(session)
    transcription = await transcription_repo.get(UUID(str(request.transcription_id)))
    if transcription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transcription not found.")

    service = QuizService()
    try:
        payload = await service.generate_from_transcription(transcription.content, request.num_questions)
    except QuizGenerationError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

    quiz_repo = QuizRepository(session)
    quiz = await quiz_repo.create_with_questions(transcription.id, payload)
    await session.commit()

    return QuizOut.model_validate(quiz)


@router.get("/quiz/{quiz_id}", response_model=QuizOut)
async def get_quiz(quiz_id: UUID, session: AsyncSession = Depends(get_db_session)) -> QuizOut:
    quiz_repo = QuizRepository(session)
    quiz = await quiz_repo.get(quiz_id)
    if quiz is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found.")
    return QuizOut.model_validate(quiz)


@router.get("/quizzes", response_model=list[QuizListItem])
async def list_quizzes(session: AsyncSession = Depends(get_db_session)) -> list[QuizListItem]:
    quiz_repo = QuizRepository(session)
    rows = await quiz_repo.list_recent()
    return [
        QuizListItem(id=row.id, title=row.title, num_questions=row.num_questions, created_at=row.created_at)
        for row in rows
    ]