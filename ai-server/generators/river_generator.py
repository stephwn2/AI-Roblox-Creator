import random

import trimesh


def create_river(
    scale: float = 1.0,
) -> trimesh.Scene:

    scene = trimesh.Scene()

    width = random.uniform(2.5, 5.0)
    length = random.uniform(12.0, 18.0)

    river = trimesh.creation.box(
        extents=(
            width,
            length,
            0.08,
        )
    )

    river.visual.face_colors = [
        70,
        130,
        220,
        255,
    ]

    river.apply_translation(
        (
            0,
            0,
            -0.04,
        )
    )

    scene.add_geometry(
        river,
        node_name="River",
    )

    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)

    return scene
