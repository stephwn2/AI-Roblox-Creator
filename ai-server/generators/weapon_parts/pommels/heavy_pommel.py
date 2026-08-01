import trimesh


def create_heavy_pommel(
    size_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a large heavy pommel."""

    pommel = trimesh.creation.icosphere(
        subdivisions=2,
        radius=0.24 * size_multiplier,
    )

    pommel.visual.face_colors = color
    pommel.apply_translation((0, 0, -0.48))

    return pommel