from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    # ==========================================
    # API KEYS
    # ==========================================

    gemini_api_key: str = Field(
        default="",
        validation_alias="GEMINI_API_KEY",
    )

    hf_token: str = Field(
        default="",
        validation_alias="HF_TOKEN",
    )

    # ==========================================
    # AI MODELS
    # ==========================================

    gemini_flash_model: str = Field(
        default="gemini-3.8-flash",
        validation_alias="GEMINI_FLASH_MODEL",
    )

    gemini_pro_model: str = Field(
        default="gemini-3.1-pro-preview",
        validation_alias="GEMINI_PRO_MODEL",
    )

    hf_image_model: str = Field(
        default="stabilityai/stable-diffusion-3-medium-diffusers",
        validation_alias="HF_IMAGE_MODEL",
    )

    hf_provider: str = Field(
        default="hf-inference",
        validation_alias="HF_PROVIDER",
    )

    # ==========================================
    # APPLICATION
    # ==========================================

    mock_mode: bool = Field(
        default=False,
        validation_alias="MOCK_MODE",
    )

    app_host: str = Field(
        default="127.0.0.1",
        validation_alias="APP_HOST",
    )

    app_port: int = Field(
        default=8000,
        validation_alias="APP_PORT",
    )

    # ==========================================
    # VALIDATION LIMITS
    # ==========================================

    max_prompt_length: int = Field(
        default=2000,
        validation_alias="MAX_PROMPT_LENGTH",
    )

    max_character_length: int = Field(
        default=80,
        validation_alias="MAX_CHARACTER_LENGTH",
    )

    max_setting_length: int = Field(
        default=120,
        validation_alias="MAX_SETTING_LENGTH",
    )

    max_tone_length: int = Field(
        default=50,
        validation_alias="MAX_TONE_LENGTH",
    )

    max_art_style_length: int = Field(
        default=80,
        validation_alias="MAX_ART_STYLE_LENGTH",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ==========================================
    # DIRECTORIES
    # ==========================================

    @property
    def static_dir(self) -> Path:
        return BASE_DIR / "app" / "static"

    @property
    def templates_dir(self) -> Path:
        return BASE_DIR / "app" / "templates"

    @property
    def panels_dir(self) -> Path:
        return self.static_dir / "panels"

    @property
    def exports_dir(self) -> Path:
        return self.static_dir / "exports"


settings = Settings()

# Create directories automatically
settings.panels_dir.mkdir(parents=True, exist_ok=True)
settings.exports_dir.mkdir(parents=True, exist_ok=True)
