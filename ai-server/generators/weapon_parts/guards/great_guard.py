import trimesh


def create_great_guard(
    width_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a large heavy greatsword crossguard."""

    guard = trimesh.creation.box(
        extents=(
            1.65 * width_multiplier,
            0.22,
            0.22,
        ),
    )

    guard.visual.face_colors = color
    guard.apply_translation((0, 0, 0.48))

    return guard