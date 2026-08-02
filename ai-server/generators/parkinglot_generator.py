import trimesh


def create_parking_lot(
    scale: float = 1.0,
) -> trimesh.Scene:

    scene = trimesh.Scene()

    asphalt = trimesh.creation.box(
        extents=(8.0, 10.0, 0.08),
    )

    asphalt.visual.face_colors = [
        70,
        70,
        70,
        255,
    ]

    scene.add_geometry(
        asphalt,
        node_name="ParkingLot",
    )

    line_color = [
        240,
        240,
        240,
        255,
    ]

    for x in (
        -3,
        -2,
        -1,
        0,
        1,
        2,
        3,
    ):

        line = trimesh.creation.box(
            extents=(
                0.05,
                8.5,
                0.02,
            )
        )

        line.visual.face_colors = line_color

        line.apply_translation(
            (
                x,
                0,
                0.05,
            )
        )

        scene.add_geometry(line)

    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)

    return scene