import trimesh


def create_katana_handle(
    length_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a long katana grip."""

    handle = trimesh.creation.cylinder(
        radius=0.11,
        height=1.35 * length_multiplier,
        sections=18,
    )

    handle.visual.face_colors = color

    return handle