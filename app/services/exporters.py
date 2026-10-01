from datetime import datetime
from pathlib import Path
import unicodedata

from fpdf import FPDF

from app.config import settings
from app.models import ComicPanel


def _ascii_safe(value: str) -> str:

    normalized = unicodedata.normalize(
        "NFKD",
        value,
    )

    return normalized.encode(
        "ascii",
        "ignore",
    ).decode("ascii")


def _local_image_path(
    browser_path: str,
) -> Path:

    prefix = "/static/"

    if not browser_path.startswith(prefix):
        raise ValueError(
            "Invalid image path."
        )

    relative = browser_path[
        len(prefix):
    ]

    path = (
        settings.static_dir / relative
    ).resolve()

    static_root = (
        settings.static_dir.resolve()
    )

    if static_root not in path.parents:
        raise ValueError(
            "Image path escapes static directory."
        )

    return path


def _text(
    pdf: FPDF,
    value: str,
    size: float = 10,
    bold: bool = False,
    italic: bool = False,
):

    style = ""

    if bold:
        style += "B"

    if italic:
        style += "I"

    pdf.set_font(
        "Helvetica",
        style=style,
        size=size,
    )

    pdf.set_x(20)

    pdf.multi_cell(
        170,
        6,
        _ascii_safe(value),
        new_x="LMARGIN",
        new_y="NEXT",
    )


def save_pdf(
    layout: list[ComicPanel],
    title: str = "ComicCraft Comic",
) -> str:

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"comiccraft_{timestamp}.pdf"
    )

    destination = (
        settings.exports_dir / filename
    )

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4",
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=12,
    )

    for panel in layout:

        pdf.add_page()

        # Panel title
        _text(
            pdf,
            (
                f"Panel {panel.panel_number}: "
                f"{panel.title}"
            ),
            size=18,
            bold=True,
        )

        # Image
        image_path = _local_image_path(
            panel.image_path
        )

        if image_path.exists():

            pdf.image(
                str(image_path),
                x=20,
                y=38,
                w=170,
            )

            pdf.set_y(158)

        # Scene
        _text(
            pdf,
            panel.scene_description,
            size=10,
            italic=True,
        )

        # Caption
        pdf.ln(2)

        _text(
            pdf,
            "Caption",
            size=11,
            bold=True,
        )

        _text(
            pdf,
            panel.caption,
        )

        # Narration
        pdf.ln(2)

        _text(
            pdf,
            "Narration",
            size=11,
            bold=True,
        )

        _text(
            pdf,
            panel.narration,
        )

        # Dialogue
        if panel.dialogue.strip():

            pdf.ln(2)

            _text(
                pdf,
                "Dialogue",
                size=11,
                bold=True,
            )

            _text(
                pdf,
                panel.dialogue,
            )

    pdf.output(
        str(destination)
    )

    return (
        f"/download/{filename}"
    )
