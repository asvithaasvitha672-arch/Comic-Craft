from app.config import settings
from app.models import ComicOutline, ComicRequest


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


def generate_outline(
    request: ComicRequest,
) -> ComicOutline:

    """
    Generate a structured five-panel comic outline.
    """

    from google.genai import types

    prompt = f"""
Create a cohesive five-panel comic outline.

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

Requirements:

1. Exactly five panels.
2. Keep the same main character throughout.
3. The story must have a clear beginning, middle and ending.
4. Every scene must be visually drawable.
5. Make each panel different but connected.
6. image_prompt must be detailed enough for an image-generation model.
7. Do not put readable text inside image_prompt.
8. Do not request speech bubbles inside the generated image.
"""

    client = _client()

    response = client.models.generate_content(
        model=settings.gemini_flash_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComicOutline,
            temperature=0.8,
        ),
    )

    if response.parsed:
        return response.parsed

    raise RuntimeError(
        "Gemini returned no structured outline."
    )
