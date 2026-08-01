import trimesh


def create_wrapped_handle(
    length_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a wrapped leather sword handle."""

    handle = trimesh.creation.cylinder(
        radius=0.13,
        height=1.05 * length_multiplier,
        sections=16,
    )

    handle.visual.face_colors = color

    return handle