import trimesh

from generators.blueprints import BuildingBlueprint
from generators.building_blueprint_builder import (
    create_building_blueprint,
)
from generators.building_parts.floor import create_building_floor
from generators.building_parts.walls import (
    create_exterior_walls,
    create_interior_wall_with_doorway,
)
from generators.building_parts.porch import create_porch


BUILDING_MATERIAL_COLORS: dict[str, dict[str, list[int]]] = {
    "wood": {
        "walls": [145, 95, 55, 255],
        "roof": [92, 58, 38, 255],
        "door": [82, 48, 28, 255],
        "windows": [105, 175, 215, 220],
        "chimney": [105, 92, 82, 255],
    },
    "stone": {
        "walls": [140, 140, 135, 255],
        "roof": [85, 88, 92, 255],
        "door": [85, 58, 38, 255],
        "windows": [105, 175, 215, 220],
        "chimney": [115, 112, 108, 255],
    },
    "brick": {
        "walls": [155, 72, 55, 255],
        "roof": [80, 48, 42, 255],
        "door": [75, 42, 25, 255],
        "windows": [105, 175, 215, 220],
        "chimney": [135, 68, 52, 255],
    },
    "gold": {
        "walls": [195, 155, 52, 255],
        "roof": [125, 92, 30, 255],
        "door": [92, 55, 28, 255],
        "windows": [130, 205, 235, 220],
        "chimney": [160, 125, 45, 255],
    },
}


def get_building_colors(
    material: str,
    condition: str,
) -> dict[str, list[int]]:
    """Return building colors for a material and condition."""

    normalized_material = material.strip().lower()
    normalized_condition = condition.strip().lower()

    base_colors = BUILDING_MATERIAL_COLORS.get(
        normalized_material,
        BUILDING_MATERIAL_COLORS["wood"],
    )

    colors = {
        name: color.copy()
        for name, color in base_colors.items()
    }

    if normalized_condition in {
        "old",
        "ancient",
        "aged",
        "weathered",
    }:
        for part_name in {
            "walls",
            "roof",
            "door",
            "chimney",
        }:
            red, green, blue, alpha = colors[part_name]

            colors[part_name] = [
                max(red - 25, 0),
                max(green - 25, 0),
                max(blue - 25, 0),
                alpha,
            ]

    elif normalized_condition in {
        "burned",
        "charred",
    }:
        colors["walls"] = [58, 50, 45, 255]
        colors["roof"] = [38, 34, 32, 255]
        colors["door"] = [42, 32, 26, 255]
        colors["chimney"] = [48, 44, 42, 255]

    return colors


def create_gable_roof(
    width: float,
    depth: float,
    roof_height: float,
    base_z: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a simple triangular-prism gable roof."""

    half_width = width / 2
    half_depth = depth / 2

    vertices = [
        [-half_width, -half_depth, base_z],
        [half_width, -half_depth, base_z],
        [-half_width, half_depth, base_z],
        [half_width, half_depth, base_z],
        [0.0, -half_depth, base_z + roof_height],
        [0.0, half_depth, base_z + roof_height],
    ]

    faces = [
        [0, 1, 4],
        [2, 5, 3],
        [0, 4, 5],
        [0, 5, 2],
        [1, 3, 5],
        [1, 5, 4],
        [0, 2, 3],
        [0, 3, 1],
    ]

    roof = trimesh.Trimesh(
        vertices=vertices,
        faces=faces,
        process=True,
    )

    roof.visual.face_colors = color

    return roof

def create_hip_roof(
    width: float,
    depth: float,
    roof_height: float,
    base_z: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a four-sided hip roof with a horizontal center ridge."""

    half_width = width / 2
    half_depth = depth / 2

    ridge_half_length = max(
    half_width * 0.18,
    0.10,
)

    vertices = [
        # Bottom corners
        [-half_width, -half_depth, base_z],  # 0 front-left
        [half_width, -half_depth, base_z],   # 1 front-right
        [half_width, half_depth, base_z],    # 2 back-right
        [-half_width, half_depth, base_z],   # 3 back-left

        # Ridge points running left-to-right
        [-ridge_half_length, 0.0, base_z + roof_height],  # 4
        [ridge_half_length, 0.0, base_z + roof_height],   # 5
    ]

    faces = [
        # Front slope
        [0, 1, 5],
        [0, 5, 4],

        # Back slope
        [3, 4, 5],
        [3, 5, 2],

        # Left triangular slope
        [0, 4, 3],

        # Right triangular slope
        [1, 2, 5],

        # Bottom closure
        [0, 3, 2],
        [0, 2, 1],
    ]

    roof = trimesh.Trimesh(
        vertices=vertices,
        faces=faces,
        process=True,
    )

    roof.visual.face_colors = color

    return roof

def create_cone_roof(
    width: float,
    depth: float,
    roof_height: float,
    base_z: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a low-poly cone roof for towers."""

    roof_radius = max(
        width,
        depth,
    ) * 0.62

    roof = trimesh.creation.cone(
        radius=roof_radius,
        height=max(
            roof_height,
            0.40,
        ),
        sections=12,
    )

    roof.visual.face_colors = color

    roof.apply_translation(
        (
            0.0,
            0.0,
            base_z,
        )
    )

    return roof

def create_flat_roof(
    width: float,
    depth: float,
    roof_height: float,
    base_z: float,
    color: list[int],
) -> trimesh.Trimesh:
    """Create a simple flat roof slab."""

    resolved_height = max(
        roof_height * 0.18,
        0.12,
    )

    roof = trimesh.creation.box(
        extents=(
            width * 1.06,
            depth * 1.06,
            resolved_height,
        ),
    )

    roof.visual.face_colors = color

    roof.apply_translation(
        (
            0.0,
            0.0,
            base_z + resolved_height / 2,
        )
    )

    return roof


def build_building_from_blueprint(
    blueprint: BuildingBlueprint,
    scale: float = 1.0,
) -> trimesh.Scene:
    """Build a hollow modular building from a completed blueprint."""

    colors = get_building_colors(
        material=blueprint.material,
        condition=blueprint.condition,
    )

    scene = trimesh.Scene()

    width = blueprint.width
    depth = blueprint.depth
    floor_height = blueprint.wall_height
    total_wall_height = floor_height * blueprint.floor_count
    wall_thickness = blueprint.wall_thickness

    doorway_width = min(
        width * 0.28,
        1.20,
    )
    doorway_height = min(
        floor_height * 0.78,
        2.20,
    )

    # Floor
    floor = create_building_floor(
        width=width,
        depth=depth,
        thickness=0.14,
        color=colors["walls"],
        z_position=0.0,
    )

    scene.add_geometry(
        floor,
        node_name="Floor",
    )

    # Hollow exterior walls with a real doorway
    exterior_walls = create_exterior_walls(
        width=width,
        depth=depth,
        height=total_wall_height,
        thickness=wall_thickness,
        doorway_width=doorway_width,
        doorway_height=doorway_height,
        color=colors["walls"],
    )

    for wall_name, wall_mesh in exterior_walls:
        scene.add_geometry(
            wall_mesh,
            node_name=wall_name,
        )

    # Interior divider with its own doorway
    interior_walls = create_interior_wall_with_doorway(
        width=width,
        height=total_wall_height,
        thickness=wall_thickness,
        doorway_width=min(
            width * 0.24,
            1.10,
        ),
        doorway_height=doorway_height,
        color=colors["walls"],
        y_position=0.0,
    )

    for wall_name, wall_mesh in interior_walls:
        scene.add_geometry(
            wall_mesh,
            node_name=wall_name,
        )

            # Large warehouse loading door
    if blueprint.building_style == "warehouse":
        loading_door_width = width * 0.48
        loading_door_height = min(
            floor_height * 0.72,
            2.8,
        )

        loading_door = trimesh.creation.box(
            extents=(
                loading_door_width,
                0.07,
                loading_door_height,
            ),
        )

        loading_door.visual.face_colors = [
            90,
            95,
            100,
            255,
        ]

        loading_door.apply_translation(
            (
                0.0,
                -(depth / 2 + 0.04),
                loading_door_height / 2,
            )
        )

        scene.add_geometry(
            loading_door,
            node_name="WarehouseLoadingDoor",
        )

        # Horizontal metal lines across the roll-up door
        panel_count = 6
        panel_height = loading_door_height / panel_count

        for panel_index in range(1, panel_count):
            panel_line = trimesh.creation.box(
                extents=(
                    loading_door_width * 0.98,
                    0.025,
                    0.025,
                ),
            )

            panel_line.visual.face_colors = [
                55,
                60,
                65,
                255,
            ]

            panel_line.apply_translation(
                (
                    0.0,
                    -(depth / 2 + 0.082),
                    panel_height * panel_index,
                )
            )

            scene.add_geometry(
                panel_line,
                node_name=f"LoadingDoorLine{panel_index}",
            )

        # Add porches to residential building styles
    if blueprint.building_style in {
        "house",
        "cabin",
        "farmhouse",
        "farm house",
        "hut",
    }:
        is_farmhouse = blueprint.building_style in {
            "farmhouse",
            "farm house",
        }

        porch_parts = create_porch(
            building_width=width,
            building_depth=depth,
            porch_width_ratio=(
                0.92
                if is_farmhouse
                else 0.68
            ),
            porch_depth=(
                1.35
                if is_farmhouse
                else 1.15
            ),
            floor_height=0.16,
            post_height=min(
                floor_height * 0.78,
                2.1,
            ),
            post_thickness=0.12,
            post_count=(
                4
                if is_farmhouse
                else 2
            ),
            color=colors["door"],
        )

        for porch_name, porch_mesh in porch_parts:
            scene.add_geometry(
                porch_mesh,
                node_name=porch_name,
            )

    # Decorative windows on the front.
    # These do not cut real holes yet.
    window_count = max(
        blueprint.window_count,
        0,
    )

    if blueprint.building_style == "warehouse":
        window_count = min(
            window_count,
            2,
    )

    if window_count > 0:
        window_width = min(
            width * 0.16,
            0.70,
        )
        window_height = min(
            floor_height * 0.28,
            0.75,
        )

        for index in range(window_count):
            side = -1.0 if index % 2 == 0 else 1.0
            floor_index = (
                index // 2
            ) % blueprint.floor_count

            window = trimesh.creation.box(
                extents=(
                    window_width,
                    0.05,
                    window_height,
                ),
            )

            window.visual.face_colors = colors["windows"]

            window.apply_translation(
                (
                    width * 0.28 * side,
                    -(depth / 2 + 0.03),
                    floor_index * floor_height
                    + floor_height * 0.58,
                )
            )

            scene.add_geometry(
                window,
                node_name=f"Window{index + 1}",
            )

    # Roof
        roof_base_z = total_wall_height



    if blueprint.roof_style in {
        "flat",
        "slab",
    }:
        roof = create_flat_roof(
            width=width,
            depth=depth,
            roof_height=blueprint.roof_height,
            base_z=roof_base_z,
            color=colors["roof"],
        )

    elif blueprint.roof_style in {
        "cone",
        "tower",
    }:
        roof = create_cone_roof(
            width=width,
            depth=depth,
            roof_height=blueprint.roof_height,
            base_z=roof_base_z,
            color=colors["roof"],
        )

    elif blueprint.roof_style == "hip":
        roof = create_hip_roof(
            width=width * 1.18,
            depth=depth * 1.18,
            roof_height=blueprint.roof_height * 1.15,
            base_z=roof_base_z,
            color=colors["roof"],
    )

    else:
        roof = create_gable_roof(
            width=width * 1.08,
            depth=depth * 1.08,
            roof_height=blueprint.roof_height,
            base_z=roof_base_z,
            color=colors["roof"],
        )

    scene.add_geometry(
        roof,
        node_name="Roof_Removable",
    )

    # Optional balcony
    if blueprint.has_balcony:
        balcony = trimesh.creation.box(
            extents=(
                width * 0.60,
                depth * 0.20,
                0.12,
            ),
        )

        balcony.visual.face_colors = colors["door"]

        balcony.apply_translation(
            (
                0.0,
                -(depth / 2 + depth * 0.10),
                floor_height * 1.05,
            )
        )

        scene.add_geometry(
            balcony,
            node_name="Balcony",
        )

    # Apply the final asset scale to every modular part.
    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)

    return scene

def create_building(
    scale: float = 1.0,
    material: str = "wood",
    style: str = "house",
    condition: str = "clean",
    size: str = "normal",
    roof_style: str = "gable",
    floor_count: int = 1,
    door_count: int = 1,
    window_count: int = 4,
    has_chimney: bool = False,
    has_balcony: bool = False,
    has_tower: bool = False,
    variation: bool = True,
) -> trimesh.Scene:
    """Create a procedural building through the blueprint pipeline."""

    blueprint = create_building_blueprint(
        building_style=style,
        material=material,
        condition=condition,
        size=size,
        roof_style=roof_style,
        floor_count=floor_count,
        door_count=door_count,
        window_count=window_count,
        has_chimney=has_chimney,
        has_balcony=has_balcony,
        has_tower=has_tower,
        variation=variation,
    )

    return build_building_from_blueprint(
        blueprint=blueprint,
        scale=scale,
    )