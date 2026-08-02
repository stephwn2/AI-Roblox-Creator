from generators.blueprints import BuildingBlueprint


def create_building_blueprint(
    building_style: str = "house",
    material: str = "wood",
    condition: str = "clean",
    size: str = "normal",
    width: float = 3.0,
    depth: float = 3.0,
    wall_height: float = 2.5,
    floor_count: int = 1,
    roof_style: str = "automatic",
    roof_height: float = 1.2,
    door_count: int = 1,
    window_count: int = 4,
    has_chimney: bool = False,
    has_balcony: bool = False,
    has_tower: bool = False,
    variation: bool = True,
) -> BuildingBlueprint:
    """Create a complete procedural building blueprint."""

    normalized_style = building_style.strip().lower()
    normalized_material = material.strip().lower()
    normalized_condition = condition.strip().lower()
    normalized_size = size.strip().lower()
    normalized_roof_style = roof_style.strip().lower()

    resolved_floor_count = max(
        int(floor_count),
        1,
    )

    resolved_door_count = max(
        int(door_count),
        0,
    )

    resolved_window_count = max(
        int(window_count),
        0,
    )

    base_wall_thickness = 0.18

    # Size modifiers
    if normalized_size == "tiny":
        width *= 0.55
        depth *= 0.55
        wall_height *= 0.65
        roof_height *= 0.75

    elif normalized_size == "small":
        width *= 0.80
        depth *= 0.80
        wall_height *= 0.82
        roof_height *= 0.90

    elif normalized_size == "large":
        width *= 1.40
        depth *= 1.40
        wall_height *= 1.30
        roof_height *= 1.20

    elif normalized_size == "giant":
        width *= 1.80
        depth *= 1.80
        wall_height *= 1.55
        roof_height *= 1.35

    elif normalized_size == "massive":
        width *= 2.20
        depth *= 2.20
        wall_height *= 1.80
        roof_height *= 1.50

    # Building-style modifiers
    if normalized_style in {
        "cabin",
        "hut",
    }:
        width *= 0.85
        depth *= 0.85
        roof_height *= 1.30
        resolved_floor_count = 1
        resolved_window_count = max(
            resolved_window_count,
            2,
        )

    elif normalized_style in {
        "watchtower",
        "tower",
    }:
        width *= 0.75
        depth *= 0.75
        wall_height *= 1.70

        resolved_floor_count = max(
            resolved_floor_count,
            3,
        )

        resolved_window_count = max(
            resolved_window_count,
            resolved_floor_count * 2,
        )

    elif normalized_style in {
        "apartment",
        "apartments",
        "apartment building",
    }:
        width *= 1.35
        depth *= 1.20
        wall_height *= 1.05

        resolved_floor_count = max(
            resolved_floor_count,
            4,
        )

        resolved_window_count = max(
            resolved_window_count,
            resolved_floor_count * 4,
        )

        normalized_roof_style = "flat"

    elif normalized_style == "warehouse":
        width *= 2.00
        depth *= 2.00
        wall_height *= 1.10

        resolved_floor_count = 1
        resolved_window_count = min(
            max(resolved_window_count, 2),
            2,
        )

        normalized_roof_style = "flat"

    elif normalized_style in {
        "castle",
        "fortress",
    }:
        width *= 1.50
        depth *= 1.50
        wall_height *= 1.25

        resolved_floor_count = max(
            resolved_floor_count,
            2,
        )

        resolved_window_count = max(
            resolved_window_count,
            resolved_floor_count * 4,
        )

    elif normalized_style in {
        "church",
        "chapel",
    }:
        width *= 1.20
        depth *= 1.55
        wall_height *= 1.35
        roof_height *= 1.65

        resolved_floor_count = max(
            resolved_floor_count,
            2,
        )

        resolved_window_count = max(
            resolved_window_count,
            6,
        )

    elif normalized_style in {
        "factory",
        "industrial",
    }:
        width *= 2.10
        depth *= 1.70
        wall_height *= 1.20

        resolved_floor_count = 1
        resolved_window_count = max(
            resolved_window_count,
            4,
        )

        normalized_roof_style = "flat"
        has_chimney = True

    # Automatic roof selection
    if normalized_roof_style in {
        "",
        "automatic",
        "default",
        "gable",
    }:
        if normalized_style in {
            "watchtower",
            "tower",
        }:
            normalized_roof_style = "cone"

        elif normalized_style in {
            "warehouse",
            "apartment",
            "apartments",
            "apartment building",
            "factory",
            "industrial",
        }:
            normalized_roof_style = "flat"

        else:
            normalized_roof_style = "gable"

    return BuildingBlueprint(
        building_style=normalized_style,
        material=normalized_material,
        condition=normalized_condition,
        size=normalized_size,
        width=width,
        depth=depth,
        wall_height=wall_height,
        floor_count=resolved_floor_count,
        roof_style=normalized_roof_style,
        roof_height=roof_height,
        door_count=resolved_door_count,
        window_count=resolved_window_count,
        has_chimney=bool(has_chimney),
        has_balcony=bool(has_balcony),
        has_tower=bool(has_tower),
        wall_thickness=base_wall_thickness,
    )