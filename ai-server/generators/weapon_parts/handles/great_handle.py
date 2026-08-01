import trimesh


def create_great_handle(
    length_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a long two-handed handle."""

    handle = trimesh.creation.cylinder(
        radius=0.15,
        height=1.70 * length_multiplier,
        sections=16,
    )

    handle.visual.face_colors = color

    return handle