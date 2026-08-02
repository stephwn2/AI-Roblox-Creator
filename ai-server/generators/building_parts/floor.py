import trimesh


def create_building_floor(
    width: float,
    depth: float,
    thickness: float,
    color: list[int],
    z_position: float = 0.0,
) -> trimesh.Trimesh:
    """Create one modular building floor slab."""

    resolved_thickness = max(
        thickness,
        0.05,
    )

    floor = trimesh.creation.box(
        extents=(
            width,
            depth,
            resolved_thickness,
        ),
    )

    floor.visual.face_colors = color

    floor.apply_translation(
        (
            0.0,
            0.0,
            z_position + resolved_thickness / 2,
        )
    )

    return floor