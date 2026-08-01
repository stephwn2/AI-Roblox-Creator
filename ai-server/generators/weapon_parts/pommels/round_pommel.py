import trimesh


def create_round_pommel(
    size_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a standard round pommel."""

    pommel = trimesh.creation.icosphere(
        subdivisions=1,
        radius=0.18 * size_multiplier,
    )

    pommel.visual.face_colors = color
    pommel.apply_translation((0, 0, -0.48))

    return pommel