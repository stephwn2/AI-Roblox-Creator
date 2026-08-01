import trimesh


def create_rapier_guard(
    width_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a rounded rapier-style hand guard."""

    guard = trimesh.creation.uv_sphere(
        radius=0.30 * width_multiplier,
        count=[16, 8],
    )

    guard.apply_scale((1.0, 0.35, 0.55))
    guard.visual.face_colors = color
    guard.apply_translation((0, 0, 0.48))

    return guard