from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator



class Settings(BaseSettings):
    DATABASE_URL: str
    BOT_TOKEN: str

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith("postgresql+asyncpg://"):
            raise ValueError("Must use asyncpg driver")
        return v

    @field_validator("BOT_TOKEN")
    @classmethod
    def validate_telegram_bot_token(cls, v: str) -> str:
        parts = v.split(":")
        if len(parts) != 2:
            raise ValueError("Token must be in format '<bot_id>:<bot_key>'")


    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

settings = Settings()