import trimesh


def create_bridge(
    scale: float = 1.0,
) -> trimesh.Scene:
    """Create a simple recognizable bridge reference."""

    scene = trimesh.Scene()

    deck_color = [110, 110, 115, 255]
    rail_color = [85, 85, 90, 255]
    support_color = [95, 95, 100, 255]

    bridge_length = 7.0
    bridge_width = 2.6
    deck_thickness = 0.25
    deck_height = 1.2

    # Main deck
    deck = trimesh.creation.box(
        extents=(
            bridge_width,
            bridge_length,
            deck_thickness,
        )
    )

    deck.visual.face_colors = deck_color

    deck.apply_translation(
        (
            0.0,
            0.0,
            deck_height,
        )
    )

    scene.add_geometry(
        deck,
        node_name="BridgeDeck",
    )

    # Support pillars
    support_positions = [
        -bridge_length * 0.30,
        bridge_length * 0.30,
    ]

    for index, y_position in enumerate(
        support_positions,
        start=1,
    ):
        for side, x_position in enumerate(
            (
                -bridge_width * 0.35,
                bridge_width * 0.35,
            ),
            start=1,
        ):
            support = trimesh.creation.box(
                extents=(
                    0.28,
                    0.42,
                    deck_height,
                )
            )

            support.visual.face_colors = support_color

            support.apply_translation(
                (
                    x_position,
                    y_position,
                    deck_height / 2,
                )
            )

            scene.add_geometry(
                support,
                node_name=f"Support{index}_{side}",
            )

    # Side rails
    rail_height = 0.65
    rail_thickness = 0.10

    for side_index, x_position in enumerate(
        (
            -bridge_width / 2,
            bridge_width / 2,
        ),
        start=1,
    ):
        top_rail = trimesh.creation.box(
            extents=(
                rail_thickness,
                bridge_length,
                rail_thickness,
            )
        )

        top_rail.visual.face_colors = rail_color

        top_rail.apply_translation(
            (
                x_position,
                0.0,
                deck_height + rail_height,
            )
        )

        scene.add_geometry(
            top_rail,
            node_name=f"TopRail{side_index}",
        )

        for post_index, y_position in enumerate(
            (
                -bridge_length / 2,
                -bridge_length / 4,
                0.0,
                bridge_length / 4,
                bridge_length / 2,
            ),
            start=1,
        ):
            rail_post = trimesh.creation.box(
                extents=(
                    rail_thickness,
                    rail_thickness,
                    rail_height,
                )
            )

            rail_post.visual.face_colors = rail_color

            rail_post.apply_translation(
                (
                    x_position,
                    y_position,
                    deck_height + rail_height / 2,
                )
            )

            scene.add_geometry(
                rail_post,
                node_name=f"RailPost{side_index}_{post_index}",
            )

    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)

    return scene