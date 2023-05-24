from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"
        env_prefix = "TINYURL2_"


settings = Settings()
