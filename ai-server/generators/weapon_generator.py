import numpy as np
import trimesh
import random

def create_sword(
    scale: float = 1.0,
    material: str = "iron",
    variation: bool = True,
) -> trimesh.Scene:
    """Create a recognizable low-poly game sword."""
    material_colors = {
        "wood": {
            "blade": [125, 78, 38, 255],
            "guard": [95, 58, 30, 255],
            "handle": [70, 42, 22, 255],
            "pommel": [95, 58, 30, 255],
        },
        "iron": {
            "blade": [175, 185, 195, 255],
            "guard": [105, 110, 120, 255],
            "handle": [82, 48, 25, 255],
            "pommel": [105, 110, 120, 255],
        },
        "gold": {
            "blade": [212, 170, 45, 255],
            "guard": [235, 195, 65, 255],
            "handle": [92, 48, 24, 255],
            "pommel": [235, 195, 65, 255],
        },
    }

    colors = material_colors.get(
        material,
        material_colors["iron"],
    )

    if variation:
            blade_length_multiplier = random.uniform(0.85, 1.20)
            blade_width_multiplier = random.uniform(0.85, 1.15)
            guard_width_multiplier = random.uniform(0.80, 1.25)
            handle_length_multiplier = random.uniform(0.85, 1.15)
            pommel_size_multiplier = random.uniform(0.80, 1.20)
    else:
            blade_length_multiplier = 1.0
            blade_width_multiplier = 1.0
            guard_width_multiplier = 1.0
            handle_length_multiplier = 1.0
            pommel_size_multiplier = 1.0

    blade_vertices = np.array([
            [-0.16 * blade_width_multiplier, -0.05, 0.00],
            [ 0.16 * blade_width_multiplier, -0.05, 0.00],
            [-0.16 * blade_width_multiplier,  0.05, 0.00],
            [ 0.16 * blade_width_multiplier,  0.05, 0.00],

            [-0.10 * blade_width_multiplier, -0.04, 2.35 * blade_length_multiplier],
            [ 0.10 * blade_width_multiplier, -0.04, 2.35 * blade_length_multiplier],
            [-0.10 * blade_width_multiplier,  0.04, 2.35 * blade_length_multiplier],
            [ 0.10 * blade_width_multiplier,  0.04, 2.35 * blade_length_multiplier],

            [0.00, -0.03, 2.75 * blade_length_multiplier],
            [0.00,  0.03, 2.75 * blade_length_multiplier],
        ])
    blade_faces = np.array([
            [0, 1, 3], [0, 3, 2],
            [0, 4, 5], [0, 5, 1],
            [2, 3, 7], [2, 7, 6],
            [0, 2, 6], [0, 6, 4],
            [1, 5, 7], [1, 7, 3],
            [4, 6, 9], [4, 9, 8],
            [5, 8, 9], [5, 9, 7],
            [4, 8, 5],
            [6, 7, 9],
        ])

    blade = trimesh.Trimesh(
            vertices=blade_vertices,
            faces=blade_faces,
            process=True,
        )
    blade.visual.face_colors = colors["blade"]
    blade.apply_translation((0, 0, 0.55))

    guard = trimesh.creation.box(
            extents=(
                1.25 * guard_width_multiplier,
                0.18,
                0.18,
            ),
        )
    guard.visual.face_colors = colors["guard"]
    guard.apply_translation((0, 0, 0.48))

    handle = trimesh.creation.cylinder(
            radius=0.13,
            height=0.85 * handle_length_multiplier,
            sections=12,
        )
    handle.visual.face_colors = colors["handle"]
    handle.apply_translation((0, 0, 0.00))

    pommel = trimesh.creation.icosphere(
            subdivisions=1,
            radius=0.20 * pommel_size_multiplier,
        )
    pommel.visual.face_colors = colors["pommel"]
    pommel.apply_translation((0, 0, -0.48))

    scene = trimesh.Scene()
    scene.add_geometry(blade, node_name="Blade")
    scene.add_geometry(guard, node_name="Guard")
    scene.add_geometry(handle, node_name="Handle")
    scene.add_geometry(pommel, node_name="Pommel")

    for geometry in scene.geometry.values():
            geometry.apply_scale(scale)



    return scene