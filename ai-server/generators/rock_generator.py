import random

import trimesh


ROCK_COLORS = {
    "normal": [120, 120, 120, 255],
    "dark": [80, 80, 80, 255],
    "light": [170, 170, 170, 255],
}


def create_rock(
    scale: float = 1.0,
    condition: str = "normal",
) -> trimesh.Scene:

    scene = trimesh.Scene()

    color = ROCK_COLORS.get(
        condition.lower(),
        ROCK_COLORS["normal"],
    )

    rock = trimesh.creation.icosphere(
        subdivisions=2,
        radius=random.uniform(0.35, 0.55),
    )

    rock.apply_scale(
        (
            random.uniform(1.0, 1.8),
            random.uniform(0.8, 1.5),
            random.uniform(0.6, 1.2),
        )
    )

    rock.visual.face_colors = color

    scene.add_geometry(
        rock,
        node_name="Rock",
    )

    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)

    return scene