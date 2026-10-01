from pathlib import Path

from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Query,
    Request,
)

from fastapi.responses import (
    FileResponse,
    HTMLResponse,
)

from fastapi.templating import (
    Jinja2Templates,
)

from app.config import settings
from app.models import ComicRequest

from app.services.comic_service import (
    generate_comic,
)

from app.services.image_generator import (
    generate_test_image,
)


router = APIRouter()

templates = Jinja2Templates(
    directory=str(
        settings.templates_dir
    )
)


# ==========================================
# CREATE REQUEST
# ==========================================

def _make_request(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
) -> ComicRequest:

    return ComicRequest(
        story_prompt=story_prompt[
            :settings.max_prompt_length
        ],

        character_name=character_name[
            :settings.max_character_length
        ],

        setting=setting[
            :settings.max_setting_length
        ],

        tone=tone[
            :settings.max_tone_length
        ],

        art_style=art_style[
            :settings.max_art_style_length
        ],
    )


# ==========================================
# HOME PAGE
# ==========================================

@router.get(
    "/",
    response_class=HTMLResponse,
)
async def home(
    request: Request,
):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "mock_mode": settings.mock_mode
        },
    )


# ==========================================
# FORM GENERATION
# ==========================================

@router.post(
    "/generate",
    response_class=HTMLResponse,
)
async def generate_form(
    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...),
):

    try:

        comic_request = _make_request(
            story_prompt,
            character_name,
            setting,
            tone,
            art_style,
        )

        layout, pdf_url = generate_comic(
            comic_request
        )

        return templates.TemplateResponse(
            request=request,

            name="comic_preview.html",

            context={
                "layout": layout,

                "pdf_url": pdf_url,

                "request_data":
                    comic_request.model_dump(),
            },
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,

            name="index.html",

            context={
                "mock_mode":
                    settings.mock_mode,

                "error":
                    str(exc),
            },

            status_code=500,
        )


# ==========================================
# JSON API
# ==========================================

@router.post(
    "/generate-comic/json"
)
async def generate_json(
    payload: ComicRequest,
):

    try:

        layout, pdf_url = generate_comic(
            payload
        )

        return {
            "success": True,

            "panels": [
                panel.model_dump()
                for panel in layout
            ],

            "pdf_url": pdf_url,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# ==========================================
# TEST IMAGE
# ==========================================

@router.get(
    "/test-image"
)
async def test_image(
    prompt: str = Query(
        ...,
        min_length=3,
        max_length=1000,
    ),
):

    try:

        image_url = generate_test_image(
            prompt
        )

        return {
            "success": True,
            "image_url": image_url,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# ==========================================
# PDF DOWNLOAD
# ==========================================

@router.get(
    "/download/{filename}"
)
async def download_pdf(
    filename: str,
):

    # Protect against path traversal
    if (
        not filename.endswith(".pdf")
        or Path(filename).name != filename
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid filename.",
        )

    path = (
        settings.exports_dir
        / filename
    )

    if not path.exists():

        raise HTTPException(
            status_code=404,
            detail="PDF not found.",
        )

    return FileResponse(
        path=str(path),

        media_type="application/pdf",

        filename=filename,
    )


# ==========================================
# EXPORT SUCCESS
# ==========================================

@router.get(
    "/export-success",
    response_class=HTMLResponse,
)
async def export_success(
    request: Request,
):

    return templates.TemplateResponse(
        request=request,

        name="export_success.html",

        context={},
    )


# ==========================================
# HEALTH CHECK
# ==========================================

@router.get(
    "/health"
)
async def health():

    return {
        "status": "ok",

        "mock_mode":
            settings.mock_mode,

        "gemini_configured":
            bool(
                settings.gemini_api_key
            ),

        "huggingface_configured":
            bool(
                settings.hf_token
            ),
    }
