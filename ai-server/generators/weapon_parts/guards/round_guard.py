import trimesh


def create_round_guard(
    width_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a simple circular guard."""

    guard = trimesh.creation.cylinder(
        radius=0.26 * width_multiplier,
        height=0.14,
        sections=24,
    )

    guard.visual.face_colors = color
    guard.apply_translation((0, 0, 0.48))

    return guard