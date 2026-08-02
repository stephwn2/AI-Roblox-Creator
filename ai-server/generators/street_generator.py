import random

import trimesh

from generators.lot_generator import (
    add_scene_with_translation,
    create_house_lot,
)


def create_street_road(
    width: float,
    length: float,
    thickness: float = 0.08,
) -> trimesh.Trimesh:
    """Create the main road for one procedural street."""

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


def create_sidewalk(
    width: float,
    length: float,
    x_position: float,
    thickness: float = 0.10,
) -> trimesh.Trimesh:
    """Create one sidewalk running beside the road."""

    sidewalk = trimesh.creation.box(
        extents=(
            width,
            length,
            thickness,
        ),
    )

    sidewalk.visual.face_colors = [
        145,
        145,
        140,
        255,
    ]

    sidewalk.apply_translation(
        (
            x_position,
            0.0,
            thickness / 2,
        )
    )

    return sidewalk


def create_street(
    lots_per_side: int = 4,
    scale: float = 1.0,
) -> trimesh.Scene:
    """Create one street with house lots on both sides."""

    scene = trimesh.Scene()

    resolved_lots_per_side = max(
        int(lots_per_side),
        1,
    )

    road_width = 5.0
    lot_spacing = 15.0
    street_length = (
        resolved_lots_per_side
        * lot_spacing
    )

    road = create_street_road(
        width=road_width,
        length=street_length,
    )

    scene.add_geometry(
        road,
        node_name="StreetRoad",
    )

    sidewalk_width = 1.2
    sidewalk_offset = (
        road_width / 2
        + sidewalk_width / 2
    )

    left_sidewalk = create_sidewalk(
        width=sidewalk_width,
        length=street_length,
        x_position=-sidewalk_offset,
    )

    right_sidewalk = create_sidewalk(
        width=sidewalk_width,
        length=street_length,
        x_position=sidewalk_offset,
    )

    scene.add_geometry(
        left_sidewalk,
        node_name="LeftSidewalk",
    )

    scene.add_geometry(
        right_sidewalk,
        node_name="RightSidewalk",
    )

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

    first_lot_y = -(
        street_length / 2
        - lot_spacing / 2
    )

    lot_x_offset = 10.0

    for lot_index in range(
        resolved_lots_per_side
    ):
        y_position = (
            first_lot_y
            + lot_index * lot_spacing
        )

        for side_index, x_position in enumerate(
            (
                -lot_x_offset,
                lot_x_offset,
            ),
            start=1,
        ):
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
                translation=(
                    x_position,
                    y_position,
                    0.0,
                ),
                name_prefix=(
                    f"Lot{lot_index + 1}"
                    f"Side{side_index}_"
                ),
            )

    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)

    return scene