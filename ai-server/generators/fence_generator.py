import trimesh


FENCE_COLORS: dict[str, list[int]] = {
    "wood": [125, 82, 45, 255],
    "dark wood": [82, 52, 30, 255],
    "white": [225, 225, 215, 255],
    "stone": [135, 135, 130, 255],
    "metal": [92, 98, 105, 255],
    "iron": [68, 72, 78, 255],
}


def create_fence_post(
    position: tuple[float, float, float],
    height: float,
    thickness: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create one vertical fence post."""

    post = trimesh.creation.box(
        extents=(
            thickness,
            thickness,
            height,
        ),
    )

    post.visual.face_colors = color

    post.apply_translation(
        (
            position[0],
            position[1],
            position[2] + height / 2,
        )
    )

    return post


def create_fence_rail(
    start_x: float,
    end_x: float,
    y_position: float,
    z_position: float,
    thickness: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create one horizontal fence rail."""

    rail_length = max(
        abs(end_x - start_x),
        0.05,
    )

    rail = trimesh.creation.box(
        extents=(
            rail_length,
            thickness,
            thickness,
        ),
    )

    rail.visual.face_colors = color

    rail.apply_translation(
        (
            (start_x + end_x) / 2,
            y_position,
            z_position,
        )
    )

    return rail


def create_fence(
    length: float = 6.0,
    height: float = 1.2,
    spacing: float = 1.5,
    thickness: float = 0.12,
    material: str = "wood",
    rail_count: int = 2,
    scale: float = 1.0,
) -> trimesh.Scene:
    """Create a straight modular fence."""

    resolved_length = max(
        float(length),
        0.5,
    )

    resolved_height = max(
        float(height),
        0.4,
    )

    resolved_spacing = max(
        float(spacing),
        0.4,
    )

    resolved_thickness = max(
        float(thickness),
        0.05,
    )

    resolved_rail_count = max(
        int(rail_count),
        1,
    )

    normalized_material = material.strip().lower()

    color = FENCE_COLORS.get(
        normalized_material,
        FENCE_COLORS["wood"],
    )

    scene = trimesh.Scene()

    post_count = max(
        int(resolved_length / resolved_spacing) + 1,
        2,
    )

    actual_spacing = (
        resolved_length
        / (post_count - 1)
    )

    start_x = -resolved_length / 2

    post_positions: list[float] = []

    for post_index in range(post_count):
        x_position = (
            start_x
            + post_index * actual_spacing
        )

        post_positions.append(x_position)

        post = create_fence_post(
            position=(
                x_position,
                0.0,
                0.0,
            ),
            height=resolved_height,
            thickness=resolved_thickness,
            color=color,
        )

        scene.add_geometry(
            post,
            node_name=f"FencePost{post_index + 1}",
        )

    rail_bottom = resolved_height * 0.35
    rail_top = resolved_height * 0.72

    if resolved_rail_count == 1:
        rail_heights = [
            resolved_height * 0.55,
        ]
    else:
        rail_heights = [
            rail_bottom
            + (
                rail_top - rail_bottom
            )
            * rail_index
            / (resolved_rail_count - 1)
            for rail_index in range(
                resolved_rail_count
            )
        ]

    for rail_index, rail_height in enumerate(
        rail_heights,
        start=1,
    ):
        rail = create_fence_rail(
            start_x=post_positions[0],
            end_x=post_positions[-1],
            y_position=0.0,
            z_position=rail_height,
            thickness=resolved_thickness * 0.75,
            color=color,
        )

        scene.add_geometry(
            rail,
            node_name=f"FenceRail{rail_index}",
        )

    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)

    return scene
