from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict, field_validator


class TranscribeResponse(BaseModel):
    transcription_id: UUID4
    duration_s: int
    preview: str


class GenerateQuizRequest(BaseModel):
    transcription_id: UUID4
    num_questions: int = 5

    @field_validator("num_questions")
    @classmethod
    def validate_num_questions(cls, value: int) -> int:
        if not 3 <= value <= 15:
            raise ValueError("num_questions must be between 3 and 15")
        return value


class QuestionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    position: int
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct: str
    explanation: str


class QuizOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    transcription_id: UUID4
    title: str
    num_questions: int
    created_at: datetime
    questions: list[QuestionOut]


class QuizListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    title: str
    num_questions: int
    created_at: datetime


class TranscriptionListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    filename: str
    duration_s: Optional[int]
    created_at: datetime
    preview: str