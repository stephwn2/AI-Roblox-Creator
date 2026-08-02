import random

import trimesh


def create_hill(
    scale: float = 1.0,
) -> trimesh.Scene:

    scene = trimesh.Scene()

    hill = trimesh.creation.icosphere(
        subdivisions=3,
        radius=random.uniform(1.5, 2.3),
    )

    hill.apply_scale(
        (
            random.uniform(1.8, 2.6),
            random.uniform(1.8, 2.6),
            random.uniform(0.55, 0.9),
        )
    )

    hill.visual.face_colors = [
        80,
        165,
        80,
        255,
    ]

    scene.add_geometry(
        hill,
        node_name="Hill",
    )

    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)

    return scene