from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routes import router


app = FastAPI(
    title="ComicCraft",

    description=(
        "AI Comic Story Creator using "
        "Gemini and Hugging Face image generation."
    ),

    version="1.0.0",
)


# ==========================================
# STATIC FILES
# ==========================================

app.mount(
    "/static",

    StaticFiles(
        directory=str(
            settings.static_dir
        )
    ),

    name="static",
)


# ==========================================
# ROUTES
# ==========================================

app.include_router(
    router
)


# ==========================================
# STARTUP
# ==========================================

@app.on_event("startup")
async def startup_event():

    settings.panels_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    settings.exports_dir.mkdir(
        parents=True,
        exist_ok=True,
    )