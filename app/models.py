from typing import List

from pydantic import BaseModel, Field, field_validator


class ComicRequest(BaseModel):
    story_prompt: str = Field(
        min_length=3,
        max_length=2000,
    )

    character_name: str = Field(
        min_length=1,
        max_length=80,
    )

    setting: str = Field(
        min_length=1,
        max_length=120,
    )

    tone: str = Field(
        min_length=1,
        max_length=50,
    )

    art_style: str = Field(
        min_length=1,
        max_length=80,
    )

    @field_validator("*")
    @classmethod
    def strip_values(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Fields cannot be empty.")

        return value


# ==========================================
# GEMINI OUTLINE
# ==========================================

class PanelOutline(BaseModel):
    panel_number: int = Field(
        ge=1,
        le=5,
    )

    title: str

    scene_description: str

    image_prompt: str


class ComicOutline(BaseModel):
    panels: List[PanelOutline] = Field(
        min_length=5,
        max_length=5,
    )


# ==========================================
# GEMINI STORY
# ==========================================

class PanelStory(BaseModel):
    panel_number: int = Field(
        ge=1,
        le=5,
    )

    narration: str

    caption: str

    dialogue: str

    image_prompt: str


class ComicStory(BaseModel):
    panels: List[PanelStory] = Field(
        min_length=5,
        max_length=5,
    )


# ==========================================
# FINAL PANEL
# ==========================================

class ComicPanel(BaseModel):

    panel_number: int

    title: str

    scene_description: str

    image_prompt: str

    narration: str

    caption: str

    dialogue: str

    image_path: str


# ==========================================
# API RESPONSE
# ==========================================

class ComicResponse(BaseModel):

    panels: List[ComicPanel]

    pdf_url: str
    