import trimesh


def create_wood_handle(
    length_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a standard wooden handle."""

    handle = trimesh.creation.cylinder(
        radius=0.13,
        height=0.85 * length_multiplier,
        sections=12,
    )

    handle.visual.face_colors = color

    return handle