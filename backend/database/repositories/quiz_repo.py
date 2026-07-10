from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.database.models import Question, Quiz


class QuizRepository:
    """Handles persistence and lookup for quizzes and questions."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_with_questions(self, transcription_id: UUID, payload: dict) -> Quiz:
        questions_payload = payload.get("questions", [])
        quiz = Quiz(
            transcription_id=transcription_id,
            title=payload.get("title", "Generated Quiz"),
            num_questions=len(questions_payload),
        )
        self.session.add(quiz)
        await self.session.flush()

        for question_data in questions_payload:
            question = Question(
                quiz_id=quiz.id,
                position=question_data["position"],
                question=question_data["question"],
                option_a=question_data["option_a"],
                option_b=question_data["option_b"],
                option_c=question_data["option_c"],
                option_d=question_data["option_d"],
                correct=question_data["correct"],
                explanation=question_data["explanation"],
            )
            self.session.add(question)

        await self.session.flush()
        return await self.get(quiz.id)

    async def get(self, quiz_id: UUID) -> Quiz | None:
        statement = (
            select(Quiz)
            .options(selectinload(Quiz.questions))
            .where(Quiz.id == quiz_id)
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_recent(self) -> list[Quiz]:
        statement = select(Quiz).order_by(Quiz.created_at.desc())
        result = await self.session.execute(statement)
        return list(result.scalars().all())