import numpy as np
import trimesh


def create_katana_blade(
    length_multiplier: float,
    width_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a curved low-poly katana blade."""

    blade_vertices = np.array([
        [-0.10 * width_multiplier, -0.035, 0.00],
        [0.10 * width_multiplier, -0.035, 0.00],
        [-0.10 * width_multiplier, 0.035, 0.00],
        [0.10 * width_multiplier, 0.035, 0.00],

        [-0.08 * width_multiplier, -0.032, 1.10 * length_multiplier],
        [0.13 * width_multiplier, -0.032, 1.10 * length_multiplier],
        [-0.08 * width_multiplier, 0.032, 1.10 * length_multiplier],
        [0.13 * width_multiplier, 0.032, 1.10 * length_multiplier],

        [-0.02 * width_multiplier, -0.028, 2.20 * length_multiplier],
        [0.18 * width_multiplier, -0.028, 2.20 * length_multiplier],
        [-0.02 * width_multiplier, 0.028, 2.20 * length_multiplier],
        [0.18 * width_multiplier, 0.028, 2.20 * length_multiplier],

        [0.14 * width_multiplier, -0.018, 2.80 * length_multiplier],
        [0.14 * width_multiplier, 0.018, 2.80 * length_multiplier],
    ])

    blade_faces = np.array([
        [0, 1, 3], [0, 3, 2],

        [0, 4, 5], [0, 5, 1],
        [2, 3, 7], [2, 7, 6],
        [0, 2, 6], [0, 6, 4],
        [1, 5, 7], [1, 7, 3],

        [4, 8, 9], [4, 9, 5],
        [6, 7, 11], [6, 11, 10],
        [4, 6, 10], [4, 10, 8],
        [5, 9, 11], [5, 11, 7],

        [8, 12, 9],
        [10, 11, 13],
        [8, 10, 13], [8, 13, 12],
        [9, 12, 13], [9, 13, 11],
    ])

    blade = trimesh.Trimesh(
        vertices=blade_vertices,
        faces=blade_faces,
        process=True,
    )

    blade.visual.face_colors = color
    blade.apply_translation((0, 0, 0.55))

    return blade