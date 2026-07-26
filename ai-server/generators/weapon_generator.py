import numpy as np
import trimesh


def create_sword(scale: float = 1.0) -> trimesh.Scene:
    """Create a recognizable low-poly game sword."""

    blade_vertices = np.array([
        [-0.16, -0.05, 0.00],
        [0.16, -0.05, 0.00],
        [-0.16, 0.05, 0.00],
        [0.16, 0.05, 0.00],

        [-0.10, -0.04, 2.35],
        [0.10, -0.04, 2.35],
        [-0.10, 0.04, 2.35],
        [0.10, 0.04, 2.35],

        [0.00, -0.03, 2.75],
        [0.00, 0.03, 2.75],
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
    blade.visual.face_colors = [175, 185, 195, 255]
    blade.apply_translation((0, 0, 0.55))

    guard = trimesh.creation.box(
        extents=(1.25, 0.18, 0.18),
    )
    guard.visual.face_colors = [105, 72, 38, 255]
    guard.apply_translation((0, 0, 0.48))

    handle = trimesh.creation.cylinder(
        radius=0.13,
        height=0.85,
        sections=12,
    )
    handle.visual.face_colors = [82, 48, 25, 255]
    handle.apply_translation((0, 0, 0.00))

    pommel = trimesh.creation.icosphere(
        subdivisions=1,
        radius=0.20,
    )
    pommel.visual.face_colors = [105, 72, 38, 255]
    pommel.apply_translation((0, 0, -0.48))

    scene = trimesh.Scene()
    scene.add_geometry(blade, node_name="Blade")
    scene.add_geometry(guard, node_name="Guard")
    scene.add_geometry(handle, node_name="Handle")
    scene.add_geometry(pommel, node_name="Pommel")

    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)
    return scene