import numpy as np
import trimesh
import random

WEAPON_STYLES = {
    "sword": {
        "blade_length": 1.0,
        "blade_width": 1.0,
        "guard_width": 1.0,
        "handle_length": 1.0,
    },

    "dagger": {
        "blade_length": 0.55,
        "blade_width": 0.75,
        "guard_width": 0.75,
        "handle_length": 0.70,
    },

    "greatsword": {
        "blade_length": 1.65,
        "blade_width": 1.20,
        "guard_width": 1.35,
        "handle_length": 1.60,
    },
    "broadsword": {
    "blade_length": 1.10,
    "blade_width": 1.55,
    "guard_width": 1.20,
    "handle_length": 1.05,
},
}

def create_handle(
    length_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create the sword handle mesh."""

    handle = trimesh.creation.cylinder(
        radius=0.13,
        height=0.85 * length_multiplier,
        sections=12,
    )

    handle.visual.face_colors = color
    handle.apply_translation((0, 0, 0.00))

    return handle
def create_guard(
    width_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create the sword guard."""

    guard = trimesh.creation.box(
        extents=(
            1.25 * width_multiplier,
            0.18,
            0.18,
        ),
    )

    guard.visual.face_colors = color
    guard.apply_translation((0, 0, 0.48))

    return guard

def create_pommel(
    size_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create the sword pommel."""

    pommel = trimesh.creation.icosphere(
        subdivisions=1,
        radius=0.20 * size_multiplier,
    )

    pommel.visual.face_colors = color
    pommel.apply_translation((0, 0, -0.48))

    return pommel


def create_blade(
    length_multiplier: float,
    width_multiplier: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create the sword blade."""

    blade_vertices = np.array([
        [-0.16 * width_multiplier, -0.05, 0.00],
        [ 0.16 * width_multiplier, -0.05, 0.00],
        [-0.16 * width_multiplier,  0.05, 0.00],
        [ 0.16 * width_multiplier,  0.05, 0.00],

        [-0.10 * width_multiplier, -0.04, 2.35 * length_multiplier],
        [ 0.10 * width_multiplier, -0.04, 2.35 * length_multiplier],
        [-0.10 * width_multiplier,  0.04, 2.35 * length_multiplier],
        [ 0.10 * width_multiplier,  0.04, 2.35 * length_multiplier],

        [0.00, -0.03, 2.75 * length_multiplier],
        [0.00,  0.03, 2.75 * length_multiplier],
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
    blade.apply_translation((0, 0, 0.55))

    return blade

def create_sword(
    scale: float = 1.0,
    material: str = "iron",
    variation: bool = True,
    style: str = "sword",
    blade_length: float = 1.0,
    blade_width: float = 1.0,
    guard_width: float = 1.0,
    handle_length: float = 1.0,
    condition: str = "clean",
):
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
    ).copy()

    if condition == "rusty":
        colors = {
            "blade": [145, 74, 38, 255],
            "guard": [115, 62, 35, 255],
            "handle": colors["handle"],
            "pommel": [105, 58, 34, 255],
        }

    style_settings = WEAPON_STYLES.get(
        style,
        WEAPON_STYLES["sword"],
    )

    if variation:
        variation_blade_length = random.uniform(0.85, 1.20)
        variation_blade_width = random.uniform(0.85, 1.15)
        variation_guard_width = random.uniform(0.80, 1.25)
        variation_handle_length = random.uniform(0.85, 1.15)
        pommel_size_multiplier = random.uniform(0.80, 1.20)
    else:
        variation_blade_length = 1.0
        variation_blade_width = 1.0
        variation_guard_width = 1.0
        variation_handle_length = 1.0
        pommel_size_multiplier = 1.0

    blade_length_multiplier = (
                style_settings["blade_length"]
                * variation_blade_length
                * blade_length
    )

    if condition == "broken":
            blade_length_multiplier = (
        style_settings["blade_length"]
        * variation_blade_length
        * blade_length
    )

    if condition == "broken":
        blade_length_multiplier *= 0.55

    blade_width_multiplier = (
        style_settings["blade_width"]
        * variation_blade_width
        * blade_width
    )

    guard_width_multiplier = (
        style_settings["guard_width"]
        * variation_guard_width
        * guard_width
    )

    handle_length_multiplier = (
        style_settings["handle_length"]
        * variation_handle_length
        * handle_length
    )

    blade = create_blade(
            length_multiplier=blade_length_multiplier,
            width_multiplier=blade_width_multiplier,
            color=colors["blade"],
    )

    guard = create_guard(
        width_multiplier=guard_width_multiplier,
        color=colors["guard"],
    )

    handle = create_handle(
        length_multiplier=handle_length_multiplier,
        color=colors["handle"],
    )

    pommel = create_pommel(
        size_multiplier=pommel_size_multiplier,
        color=colors["pommel"],
    )

    scene = trimesh.Scene()
    scene.add_geometry(blade, node_name="Blade")
    scene.add_geometry(guard, node_name="Guard")
    scene.add_geometry(handle, node_name="Handle")
    scene.add_geometry(pommel, node_name="Pommel")

    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)

    return scene