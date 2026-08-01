import trimesh


def create_gem_pommel(
    size_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a faceted gem-like pommel."""

    pommel = trimesh.creation.icosphere(
        subdivisions=1,
        radius=0.15 * size_multiplier,
    )

    pommel.apply_scale((0.85, 0.85, 1.25))
    pommel.visual.face_colors = color
    pommel.apply_translation((0, 0, -0.48))

    return pommel