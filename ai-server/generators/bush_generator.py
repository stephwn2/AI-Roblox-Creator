import random

import trimesh


BUSH_COLORS = {
    "healthy": [55, 140, 60, 255],
    "dry": [150, 130, 70, 255],
    "dead": [95, 90, 80, 255],
}


def create_bush(
    scale: float = 1.0,
    condition: str = "healthy",
) -> trimesh.Scene:
    """Create a simple procedural bush reference."""

    scene = trimesh.Scene()

    color = BUSH_COLORS.get(
        condition.lower(),
        BUSH_COLORS["healthy"],
    )

    sphere_count = random.randint(4, 7)

    for index in range(sphere_count):

        radius = random.uniform(
            0.18,
            0.35,
        )

        sphere = trimesh.creation.icosphere(
            subdivisions=2,
            radius=radius,
        )

        sphere.visual.face_colors = color

        sphere.apply_translation(
            (
                random.uniform(-0.35, 0.35),
                random.uniform(-0.35, 0.35),
                random.uniform(
                    radius * 0.7,
                    radius * 2.0,
                ),
            )
        )

        scene.add_geometry(
            sphere,
            node_name=f"BushSphere{index}",
        )

    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)

    return scene
