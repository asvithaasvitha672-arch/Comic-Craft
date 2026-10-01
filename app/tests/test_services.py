from pathlib import Path
import hashlib

from PIL import Image

from app.config import settings

from app.models import (
    ComicOutline,
    ComicRequest,
    ComicStory,
    PanelOutline,
    PanelStory,
)

from app.services.exporters import (
    save_pdf,
)

from app.services.image_generator import (
    _mock_image,
)

from app.services.comic_service import (
    _mock_outline,
)

from app.services.layout_builder import (
    build_comic_layout,
)


def sample_data():

    # ======================================
    # SAMPLE OUTLINE
    # ======================================

    outline = ComicOutline(

        panels=[

            PanelOutline(

                panel_number=i,

                title=f"Panel {i}",

                scene_description="A scene.",

                image_prompt="A comic scene.",
            )

            for i in range(1, 6)
        ]
    )


    # ======================================
    # SAMPLE STORY
    # ======================================

    story = ComicStory(

        panels=[

            PanelStory(

                panel_number=i,

                narration="Narration.",

                caption="Caption.",

                dialogue="Hello!",

                image_prompt="A comic scene.",
            )

            for i in range(1, 6)
        ]
    )


    # ======================================
    # TEST IMAGES
    # ======================================

    images = []


    for i in range(1, 6):

        path = (
            settings.panels_dir
            / f"test_{i}.png"
        )

        Image.new(
            "RGB",
            (100, 100),
            "white",
        ).save(path)


        images.append(
            f"/static/panels/test_{i}.png"
        )


    return (
        outline,
        story,
        images,
    )


def test_layout_has_five_panels():

    outline, story, images = (
        sample_data()
    )

    layout = build_comic_layout(
        outline,
        story,
        images,
    )

    assert len(layout) == 5

    assert (
        layout[0].panel_number
        == 1
    )


def test_mock_outline_includes_user_description_in_every_image_prompt():

    request = ComicRequest(
        story_prompt="A fox discovers a glowing doorway in the forest.",
        character_name="Milo",
        setting="Forest",
        tone="Mysterious",
        art_style="Comic Book",
    )

    outline = _mock_outline(request)

    assert len(outline.panels) == 5
    assert all(
        request.story_prompt in panel.image_prompt
        for panel in outline.panels
    )
    assert len(
        {panel.image_prompt for panel in outline.panels}
    ) == 5
    assert len(
        {panel.scene_description for panel in outline.panels}
    ) == 5


def test_pdf_export():

    outline, story, images = (
        sample_data()
    )

    layout = build_comic_layout(
        outline,
        story,
        images,
    )

    pdf_url = save_pdf(
        layout
    )

    filename = Path(
        pdf_url
    ).name

    pdf_path = (
        settings.exports_dir
        / filename
    )

    assert pdf_path.exists()

    assert (
        pdf_path.stat().st_size
        > 100
    )


def test_mock_images_are_distinct_per_panel(tmp_path):

    image_hashes = set()

    for panel_number in range(1, 6):

        image_path = (
            tmp_path / f"panel_{panel_number}.png"
        )

        _mock_image(
            image_path,
            f"A comic scene in panel {panel_number}.",
            panel_number,
        )

        image_hashes.add(
            hashlib.sha256(
                image_path.read_bytes()
            ).hexdigest()
        )

    assert len(image_hashes) == 5
    