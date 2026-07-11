from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file="backend/.env", extra="ignore")

    database_url: str = "postgresql+asyncpg://quiz_user:quiz_pass@localhost:5432/quiz_db"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    cors_origins: str = "http://localhost:3000"
    whisper_model: str = "whisper-1"
    upload_max_bytes: int = 200 * 1024 * 1024

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        """Convert generic Postgres URLs into the async SQLAlchemy form."""

        if isinstance(value, str):
            if value.startswith("postgres://"):
                return value.replace("postgres://", "postgresql+asyncpg://", 1)
            if value.startswith("postgresql://") and "+asyncpg" not in value:
                return value.replace("postgresql://", "postgresql+asyncpg://", 1)
        return value

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return the cached settings instance for the application."""

    return Settings()
