import trimesh


def create_rapier_handle(
    length_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a thin rapier grip."""

    handle = trimesh.creation.cylinder(
        radius=0.08,
        height=0.90 * length_multiplier,
        sections=16,
    )

    handle.visual.face_colors = color

    return handle