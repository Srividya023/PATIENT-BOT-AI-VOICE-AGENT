from __future__ import annotations

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.phone_guard import ASSESSMENT_NUMBER, normalize_phone_number


class Settings(BaseSettings):
    voice_provider: str = Field(default="vapi", alias="VOICE_PROVIDER")
    vapi_api_key: str = Field(default="", alias="VAPI_API_KEY")
    vapi_assistant_id: str = Field(default="", alias="VAPI_ASSISTANT_ID")
    vapi_phone_number_id: str = Field(default="", alias="VAPI_PHONE_NUMBER_ID")
    vapi_base_url: str = Field(default="https://api.vapi.ai", alias="VAPI_BASE_URL")
    allowed_target_number: str = Field(default=ASSESSMENT_NUMBER, alias="ALLOWED_TARGET_NUMBER")
    dry_run: bool = Field(default=True, alias="DRY_RUN")
    poll_interval_seconds: int = Field(default=10, alias="POLL_INTERVAL_SECONDS")
    poll_timeout_seconds: int = Field(default=600, alias="POLL_TIMEOUT_SECONDS")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("allowed_target_number")
    @classmethod
    def normalize_allowed_target(cls, value: str) -> str:
        return normalize_phone_number(value)

    @field_validator("voice_provider")
    @classmethod
    def validate_voice_provider(cls, value: str) -> str:
        normalized = value.lower().strip()
        if normalized != "vapi":
            raise ValueError("VOICE_PROVIDER must be 'vapi' in this project.")
        return normalized
