from app.config import settings

from app.models import (
    ComicPanel,
    ComicRequest,
    ComicStory,
    ComicOutline,
)

from app.services.exporters import save_pdf
from app.services.gemini_flash import (
    generate_outline,
)
from app.services.gemini_pro import (
    generate_story,
)
from app.services.image_generator import (
    generate_image,
)
from app.services.layout_builder import (
    build_comic_layout,
)


# ==========================================
# MOCK OUTLINE
# ==========================================

def _mock_outline(
    request: ComicRequest,
) -> ComicOutline:

    from app.models import PanelOutline

    titles = [
        "The Beginning",
        "A Strange Discovery",
        "The Challenge",
        "The Turning Point",
        "A New Dawn",
    ]
    panel_beats = [
        "wide establishing shot introducing the story",
        "close-up discovery of the story's key clue",
        "rising action as a complication appears",
        "climactic decisive action that changes the situation",
        "warm resolution showing the story's outcome",
    ]

    panels = []

    for i in range(5):

        panels.append(
            PanelOutline(
                panel_number=i + 1,

                title=titles[i],

                scene_description=(
                    f"{panel_beats[i].capitalize()}. "
                    f"{request.story_prompt} "
                    f"Featuring {request.character_name} "
                    f"in {request.setting}."
                ),

                image_prompt=(
                    f"Illustrate a {panel_beats[i]} based on "
                    f"this story: {request.story_prompt}, "
                    f"{request.character_name}, "
                    f"{request.setting}, "
                    f"{request.art_style}, "
                    f"{request.tone}, "
                    f"cinematic comic illustration, "
                    f"panel {i + 1}, "
                    "consistent character design, "
                    "no readable text"
                ),
            )
        )

    return ComicOutline(
        panels=panels
    )


# ==========================================
# MOCK STORY
# ==========================================

def _mock_story(
    request: ComicRequest,
    outline: ComicOutline,
) -> ComicStory:

    from app.models import PanelStory

    panels = []

    for panel in outline.panels:

        panels.append(
            PanelStory(
                panel_number=panel.panel_number,

                narration=(
                    f"{request.character_name} "
                    "moves through the scene, "
                    "following a mysterious clue "
                    "and gathering courage."
                ),

                caption=(
                    "Meanwhile, the adventure "
                    f"continues in {request.setting}."
                ),

                dialogue=(
                    f"{request.character_name}: "
                    "I have to keep going. "
                    "Something important is waiting ahead."
                ),

                image_prompt=panel.image_prompt,
            )
        )

    return ComicStory(
        panels=panels
    )


# ==========================================
# COMPLETE PIPELINE
# ==========================================

def generate_comic(
    request: ComicRequest,
) -> tuple[list[ComicPanel], str]:

    # ======================================
    # STEP 1 — STORY OUTLINE
    # ======================================

    if settings.mock_mode:

        outline = _mock_outline(
            request
        )

        story = _mock_story(
            request,
            outline,
        )

    else:

        outline = generate_outline(
            request
        )

        # ==================================
        # STEP 2 — DETAILED STORY
        # ==================================

        story = generate_story(
            request,
            outline,
        )

    # ======================================
    # STEP 3 — GENERATE IMAGES
    # ======================================

    image_paths = []

    for panel in story.panels:

        image_path = generate_image(
            panel.image_prompt,
            panel.panel_number,
        )

        image_paths.append(
            image_path
        )

    # ======================================
    # STEP 4 — BUILD LAYOUT
    # ======================================

    layout = build_comic_layout(
        outline,
        story,
        image_paths,
    )

    # ======================================
    # STEP 5 — EXPORT PDF
    # ======================================

    pdf_url = save_pdf(
        layout,
        title=(
            f"{request.character_name}'s Comic"
        ),
    )

    return layout, pdf_url
