"""Application settings."""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Production application settings from environment."""

    database_url: str

    class Config:
        """Pydantic settings configuration."""

        env_file = ".env"
        env_prefix = "TINYURL2_"


settings = Settings()
