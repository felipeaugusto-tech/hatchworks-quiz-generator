from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.database.models import Base
from backend.database.connection import engine
from backend.routers import quiz, transcription


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


settings = get_settings()
app = FastAPI(title="HatchWorks Quiz API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(transcription.router)
app.include_router(quiz.router)


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}