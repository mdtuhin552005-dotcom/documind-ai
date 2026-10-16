from functools import cached_property
from pathlib import Path

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    gemini_api_key: SecretStr | None = None
    google_client_id: str | None = None
    chat_model: str = "gemini-3.5-flash-lite"
    embedding_model: str = "models/gemini-embedding-001"
    data_dir: Path = Path("./data")
    max_upload_mb: int = Field(default=15, ge=1, le=100)
    max_pdf_pages: int = Field(default=500, ge=1, le=5000)
    chunk_size: int = Field(default=1100, ge=200, le=8000)
    chunk_overlap: int = Field(default=180, ge=0, le=2000)
    retrieval_k: int = Field(default=5, ge=1, le=20)
    allowed_origins: str = ""
    log_level: str = "INFO"

    @model_validator(mode="after")
    def validate_chunk_overlap(self) -> "Settings":
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE")
        return self

    @cached_property
    def upload_limit_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024

    @cached_property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

    @cached_property
    def chroma_dir(self) -> Path:
        return self.data_dir / "chroma"

    @cached_property
    def uploads_dir(self) -> Path:
        return self.data_dir / "uploads"

    @cached_property
    def database_path(self) -> Path:
        return self.data_dir / "documind.sqlite3"


settings = Settings()
