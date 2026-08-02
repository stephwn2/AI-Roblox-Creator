import random
import trimesh

from generators.lot_generator import (
    add_scene_with_translation,
    create_house_lot,
)


def create_road(
    width: float,
    length: float,
    thickness: float = 0.08,
) -> trimesh.Trimesh:
    """Create one simple neighborhood road."""

    road = trimesh.creation.box(
        extents=(
            width,
            length,
            thickness,
        ),
    )

    road.visual.face_colors = [
        58,
        60,
        64,
        255,
    ]

    road.apply_translation(
        (
            0.0,
            0.0,
            thickness / 2,
        )
    )

    return road


def create_neighborhood(
    lot_count: int = 4,
    scale: float = 1.0,
) -> trimesh.Scene:
    """Create a small neighborhood from multiple house lots."""

    scene = trimesh.Scene()

    road_width = 5.0
    road_length = 34.0

    road = create_road(
        width=road_width,
        length=road_length,
    )

    scene.add_geometry(
        road,
        node_name="MainRoad",
    )

    lot_positions = [
        (-9.0, -8.5, 0.0),
        (9.0, -8.5, 0.0),
        (-9.0, 8.5, 0.0),
        (9.0, 8.5, 0.0),
    ]

    resolved_lot_count = min(
        max(int(lot_count), 1),
        len(lot_positions),
    )

    import random

    building_styles = [
        "house",
        "cabin",
        "house",
        "apartment",
    ]

    building_materials = [
        "wood",
        "brick",
        "stone",
    ]

    building_sizes = [
        "small",
        "normal",
        "normal",
        "large",
    ]

    for lot_index in range(resolved_lot_count):
        selected_style = random.choice(
            building_styles
        )

        selected_material = random.choice(
            building_materials
        )

        selected_size = random.choice(
            building_sizes
        )

        selected_tree_count = random.randint(
            1,
            4,
        )

        lot_scene = create_house_lot(
            scale=0.75,
            building_style=selected_style,
            building_material=selected_material,
            condition="clean",
            size=selected_size,
            fence_material="wood",
            tree_count=selected_tree_count,
        )

        add_scene_with_translation(
            target_scene=scene,
            source_scene=lot_scene,
            translation=lot_positions[lot_index],
            name_prefix=f"Lot{lot_index + 1}_",
        )

    for lot_index in range(resolved_lot_count):
        lot_scene = create_house_lot(
            scale=0.75,
            building_style=selected_style,
            building_material="wood",
            condition="clean",
            size="normal",
            fence_material="wood",
            tree_count=2,
        )

        add_scene_with_translation(
            target_scene=scene,
            source_scene=lot_scene,
            translation=lot_positions[lot_index],
            name_prefix=f"Lot{lot_index + 1}_",
        )

    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)

    return scene