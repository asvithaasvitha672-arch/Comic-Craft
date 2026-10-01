from app.models import (
    ComicOutline,
    ComicStory,
    ComicPanel,
)


def build_comic_layout(
    outline: ComicOutline,
    story: ComicStory,
    image_paths: list[str],
) -> list[ComicPanel]:

    if (
        len(outline.panels) != 5
        or len(story.panels) != 5
        or len(image_paths) != 5
    ):
        raise ValueError(
            "Comic layout requires exactly five panels."
        )

    story_by_number = {
        panel.panel_number: panel
        for panel in story.panels
    }

    layout = []

    for outline_panel in outline.panels:

        story_panel = story_by_number.get(
            outline_panel.panel_number
        )

        if not story_panel:

            raise ValueError(
                "Missing story content for "
                f"panel {outline_panel.panel_number}."
            )

        layout.append(
            ComicPanel(
                panel_number=(
                    outline_panel.panel_number
                ),

                title=outline_panel.title,

                scene_description=(
                    outline_panel.scene_description
                ),

                image_prompt=(
                    story_panel.image_prompt
                    or outline_panel.image_prompt
                ),

                narration=story_panel.narration,

                caption=story_panel.caption,

                dialogue=story_panel.dialogue,

                image_path=(
                    image_paths[
                        outline_panel.panel_number - 1
                    ]
                ),
            )
        )

    return layout
