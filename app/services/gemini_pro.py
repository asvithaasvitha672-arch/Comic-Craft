from app.config import settings
from app.models import (
    ComicOutline,
    ComicRequest,
    ComicStory,
)


def _client():

    try:
        from google import genai

    except ImportError as exc:
        raise RuntimeError(
            "google-genai is not installed. "
            "Run: pip install -r requirements.txt"
        ) from exc

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Add it to .env or enable MOCK_MODE."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_story(
    request: ComicRequest,
    outline: ComicOutline,
) -> ComicStory:

    """
    Expand the outline into:
    - narration
    - captions
    - dialogue
    - image prompts
    """

    from google.genai import types

    outline_json = outline.model_dump_json(
        indent=2
    )

    prompt = f"""
Expand this comic outline into a polished five-panel comic script.

USER INFORMATION

Story idea:
{request.story_prompt}

Main character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}


OUTLINE

{outline_json}


For every panel provide:

narration:
1-3 concise sentences describing the action or emotion.

caption:
A short cinematic or environmental caption.

dialogue:
Natural character dialogue.

If no spoken dialogue is appropriate,
use an empty string.

image_prompt:
A detailed visual prompt for an image-generation model.

Important:

- Keep the character visually consistent.
- Keep clothing and appearance consistent.
- Keep the environment consistent.
- Keep the selected art style consistent.
- Do not place readable text inside generated artwork.
- Do not include speech bubbles in the image prompt.
- Exactly five panels are required.
"""

    client = _client()

    response = client.models.generate_content(
        model=settings.gemini_pro_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComicStory,
            temperature=0.85,
        ),
    )

    if response.parsed:
        return response.parsed

    raise RuntimeError(
        "Gemini returned no structured story."
    )
