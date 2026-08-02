import trimesh


def create_porch(
    building_width: float,
    building_depth: float,
    porch_width_ratio: float = 0.65,
    porch_depth: float = 1.1,
    floor_height: float = 0.16,
    post_height: float = 2.0,
    post_thickness: float = 0.12,
    post_count: int = 2,
    color: list[int] | None = None,
) -> list[tuple[str, trimesh.Trimesh]]:
    """Create a modular front porch."""

    if color is None:
        color = [120, 78, 45, 255]

    porch_parts: list[tuple[str, trimesh.Trimesh]] = []

    porch_width = max(
        building_width * porch_width_ratio,
        1.5,
    )

    front_y = -(
        building_depth / 2
        + porch_depth / 2
    )

    porch_floor = trimesh.creation.box(
        extents=(
            porch_width,
            porch_depth,
            floor_height,
        ),
    )

    porch_floor.visual.face_colors = color

    porch_floor.apply_translation(
        (
            0.0,
            front_y,
            floor_height / 2,
        )
    )

    porch_parts.append(
        (
            "PorchFloor",
            porch_floor,
        )
    )

    step_depth = porch_depth * 0.35
    step_height = floor_height * 0.55

    front_step = trimesh.creation.box(
        extents=(
            porch_width * 0.55,
            step_depth,
            step_height,
        ),
    )

    front_step.visual.face_colors = color

    front_step.apply_translation(
        (
            0.0,
            front_y - porch_depth / 2 - step_depth / 2,
            step_height / 2,
        )
    )

    porch_parts.append(
        (
            "PorchStep",
            front_step,
        )
    )

    post_x_offset = porch_width * 0.42
    post_y_position = front_y - porch_depth * 0.30

    resolved_post_count = max(
        int(post_count),
        2,
    )

    if resolved_post_count == 2:
        post_positions = [
            -post_x_offset,
            post_x_offset,
        ]
    else:
        post_positions = [
            -post_x_offset
            + (
                post_x_offset * 2
            )
            * post_index
            / (resolved_post_count - 1)
            for post_index in range(
                resolved_post_count
            )
        ]

    for post_index, x_position in enumerate(
        post_positions,
        start=1,
    ):
        post = trimesh.creation.box(
            extents=(
                post_thickness,
                post_thickness,
                post_height,
            ),
        )

        post.visual.face_colors = color

        post.apply_translation(
            (
                x_position,
                post_y_position,
                floor_height + post_height / 2,
            )
        )

        porch_parts.append(
            (
                f"PorchPost{post_index}",
                post,
            )
        )

    roof_thickness = 0.14

    porch_roof = trimesh.creation.box(
        extents=(
            porch_width * 1.08,
            porch_depth * 1.12,
            roof_thickness,
        ),
    )

    porch_roof.visual.face_colors = color

    porch_roof.apply_translation(
        (
            0.0,
            front_y,
            floor_height + post_height,
        )
    )

    porch_parts.append(
        (
            "PorchRoof",
            porch_roof,
        )
    )

    return porch_parts