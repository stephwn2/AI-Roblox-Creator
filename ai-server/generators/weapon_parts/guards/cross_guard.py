import trimesh


def create_cross_guard(
    width_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a standard straight crossguard."""

    guard = trimesh.creation.box(
        extents=(
            1.25 * width_multiplier,
            0.18,
            0.18,
        ),
    )

    guard.visual.face_colors = color
    guard.apply_translation((0, 0, 0.48))

    return guard