import numpy as np
import trimesh


def create_shortsword_blade(
    length_multiplier: float,
    width_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a compact low-poly shortsword blade."""

    blade_length = 2.25
    base_width = 0.15
    upper_width = 0.09
    thickness = 0.048
    shoulder_height = blade_length * 0.82

    blade_vertices = np.array([
        [-base_width * width_multiplier, -thickness, 0.00],
        [ base_width * width_multiplier, -thickness, 0.00],
        [-base_width * width_multiplier,  thickness, 0.00],
        [ base_width * width_multiplier,  thickness, 0.00],

        [-upper_width * width_multiplier, -thickness * 0.80, shoulder_height * length_multiplier],
        [ upper_width * width_multiplier, -thickness * 0.80, shoulder_height * length_multiplier],
        [-upper_width * width_multiplier,  thickness * 0.80, shoulder_height * length_multiplier],
        [ upper_width * width_multiplier,  thickness * 0.80, shoulder_height * length_multiplier],

        [0.00, -thickness * 0.55, blade_length * length_multiplier],
        [0.00,  thickness * 0.55, blade_length * length_multiplier],
    ])

    blade_faces = np.array([
        [0,1,3],[0,3,2],
        [0,4,5],[0,5,1],
        [2,3,7],[2,7,6],
        [0,2,6],[0,6,4],
        [1,5,7],[1,7,3],
        [4,6,9],[4,9,8],
        [5,8,9],[5,9,7],
        [4,8,5],
        [6,7,9],
    ])

    blade = trimesh.Trimesh(
        vertices=blade_vertices,
        faces=blade_faces,
        process=True,
    )

    blade.visual.face_colors = color
    blade.apply_translation((0,0,0.55))

    return blade