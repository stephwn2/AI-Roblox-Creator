import trimesh


def create_flat_pommel(
    size_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a flat katana-style end cap."""

    pommel = trimesh.creation.cylinder(
        radius=0.13 * size_multiplier,
        height=0.12 * size_multiplier,
        sections=18,
    )

    pommel.visual.face_colors = color
    pommel.apply_translation((0, 0, -0.48))

    return pommel