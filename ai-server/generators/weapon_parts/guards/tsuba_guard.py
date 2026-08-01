import trimesh


def create_tsuba_guard(
    width_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a traditional circular katana guard."""

    guard = trimesh.creation.cylinder(
        radius=0.34 * width_multiplier,
        height=0.08,
        sections=32,
    )

    guard.visual.face_colors = color
    guard.apply_translation((0, 0, 0.48))

    return guard