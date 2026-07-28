import trimesh


def create_axe(
    scale: float = 1.0,
    material: str = "iron",
    style: str = "axe",
) -> trimesh.Scene:
    """Create a simple low-poly axe."""

    material_colors = {
        "wood": {
            "handle": [110, 68, 35, 255],
            "head": [125, 78, 38, 255],
        },
        "iron": {
            "handle": [110, 68, 35, 255],
            "head": [175, 185, 195, 255],
        },
        "gold": {
            "handle": [110, 68, 35, 255],
            "head": [212, 170, 45, 255],
        },
    }

    colors = material_colors.get(
        material,
        material_colors["iron"],
    )

    if style == "hatchet":
        handle_length = 1.35
        head_width = 0.70
        head_height = 0.42

    elif style == "battle":
        handle_length = 2.8
        head_width = 1.25
        head_height = 0.72

    elif style == "double":
        handle_length = 2.6
        head_width = 0.95
        head_height = 0.65

    else:
        handle_length = 2.3
        head_width = 0.95
        head_height = 0.55

    handle = trimesh.creation.cylinder(
        radius=0.10,
        height=handle_length,
        sections=12,
    )
    handle.visual.face_colors = colors["handle"]

    axe_head = trimesh.creation.box(
        extents=(
            head_width,
            0.22,
            head_height,
        ),
    )
    axe_head.visual.face_colors = colors["head"]
    axe_head.apply_translation(
        (
            head_width * 0.35,
            0.0,
            handle_length * 0.35,
        )
    )

    scene = trimesh.Scene()
    scene.add_geometry(
        handle,
        node_name="AxeHandle",
    )
    scene.add_geometry(
        axe_head,
        node_name="AxeHead",
    )

    if style == "double":
        second_head = trimesh.creation.box(
            extents=(
                head_width,
                0.22,
                head_height,
            ),
        )
        second_head.visual.face_colors = colors["head"]
        second_head.apply_translation(
            (
                -head_width * 0.35,
                0.0,
                handle_length * 0.35,
            )
        )

        scene.add_geometry(
            second_head,
            node_name="AxeHeadRight",
        )

    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)

    return scene