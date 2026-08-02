from dataclasses import dataclass
from typing import Any


from dataclasses import dataclass
from typing import Any


@dataclass
class BuildingBlueprint:
    """Structured instructions for one procedural building."""

    building_style: str = "house"
    material: str = "wood"
    condition: str = "clean"
    size: str = "normal"

    width: float = 3.0
    depth: float = 3.0
    wall_height: float = 2.5

    floor_count: int = 1

    roof_style: str = "gable"
    roof_height: float = 1.2

    door_count: int = 1
    window_count: int = 4

    has_chimney: bool = False
    has_balcony: bool = False
    has_tower: bool = False

    wall_thickness: float = 0.18

@dataclass
class WeaponBlueprint:
    """Structured instructions for building a weapon."""

    object_type: str = "sword"

    style: str = "sword"
    material: str = "iron"
    condition: str = "clean"
    size: str = "normal"

    scale: float = 1.0
    quantity: int = 1

    blade_length: float = 1.0
    blade_width: float = 1.0
    guard_width: float = 1.0
    handle_length: float = 1.0

    blade_style: str = "automatic"
    guard_style: str = "automatic"
    handle_style: str = "automatic"
    pommel_style: str = "automatic"

    blade_material: str = "automatic"
    guard_material: str = "automatic"
    handle_material: str = "automatic"
    pommel_material: str = "automatic"

    blade_attachment: str = "none"
    guard_attachment: str = "none"
    handle_attachment: str = "none"
    pommel_attachment: str = "none"

    blade_pattern: str = "none"
    handle_pattern: str = "none"

    engraving: str = "none"

    gemstone: str = "none"


def size_to_scale(size: str) -> float:
    """Convert a size word into a model scale multiplier."""

    normalized_size = size.strip().lower()

    size_multipliers = {
        "tiny": 0.40,
        "small": 0.70,
        "normal": 1.00,
        "large": 1.30,
        "big": 1.30,
        "giant": 1.75,
        "massive": 2.00,
        "huge": 2.00,
    }

    return size_multipliers.get(
        normalized_size,
        1.00,
    )

def get_automatic_weapon_parts(
    style: str,
) -> dict[str, str]:
    """Choose default modular parts for a weapon style."""

    normalized_style = style.strip().lower()

    part_presets = {
        "katana": {
            "blade_style": "katana",
            "guard_style": "tsuba",
            "handle_style": "katana",
            "pommel_style": "flat",
        },
        "rapier": {
            "blade_style": "rapier",
            "guard_style": "rapier",
            "handle_style": "rapier",
            "pommel_style": "gem",
        },
        "greatsword": {
            "blade_style": "greatsword",
            "guard_style": "great",
            "handle_style": "great",
            "pommel_style": "heavy",
        },
        "longsword": {
            "blade_style": "longsword",
            "guard_style": "cross",
            "handle_style": "wrapped",
            "pommel_style": "round",
        },
        "broadsword": {
            "blade_style": "broadsword",
            "guard_style": "cross",
            "handle_style": "wrapped",
            "pommel_style": "round",
        },
        "shortsword": {
            "blade_style": "shortsword",
            "guard_style": "cross",
            "handle_style": "wood",
            "pommel_style": "round",
        },
        "dagger": {
            "blade_style": "dagger",
            "guard_style": "cross",
            "handle_style": "wood",
            "pommel_style": "round",
        },
        "sword": {
            "blade_style": "sword",
            "guard_style": "cross",
            "handle_style": "wood",
            "pommel_style": "round",
        },
    }

    return part_presets.get(
        normalized_style,
        part_presets["sword"],
    ).copy()

def create_weapon_blueprint(
    style: str = "sword",
    material: str = "iron",
    condition: str = "clean",
    size: str = "normal",
    scale: float = 1.0,
    quantity: int = 1,
    blade_length: float = 1.0,
    blade_width: float = 1.0,
    guard_width: float = 1.0,
    handle_length: float = 1.0,
    blade_style: str = "automatic",
    guard_style: str = "automatic",
    handle_style: str = "automatic",
    pommel_style: str = "automatic",
    blade_material: str = "automatic",
    guard_material: str = "automatic",
    handle_material: str = "automatic",
    pommel_material: str = "automatic",
    blade_attachment: str = "none",
    guard_attachment: str = "none",
    handle_attachment: str = "none",
    pommel_attachment: str = "none",
    blade_pattern: str = "none",
    handle_pattern: str = "none",
    engraving: str = "none",
    gemstone: str = "none",
) -> WeaponBlueprint:
    """Create a normalized modular weapon blueprint."""

    normalized_style = style.strip().lower()
    normalized_material = material.strip().lower()
    normalized_condition = condition.strip().lower()
    normalized_size = size.strip().lower()

    automatic_parts = get_automatic_weapon_parts(
        style=normalized_style,
    )

    resolved_blade_style = (
        automatic_parts["blade_style"]
        if blade_style == "automatic"
        else blade_style.strip().lower()
    )

    resolved_guard_style = (
        automatic_parts["guard_style"]
        if guard_style == "automatic"
        else guard_style.strip().lower()
    )

    resolved_handle_style = (
        automatic_parts["handle_style"]
        if handle_style == "automatic"
        else handle_style.strip().lower()
    )

    resolved_pommel_style = (
        automatic_parts["pommel_style"]
        if pommel_style == "automatic"
        else pommel_style.strip().lower()
    )

    return WeaponBlueprint(
        object_type="sword",
        style=normalized_style,
        material=normalized_material,
        condition=normalized_condition,
        size=normalized_size,
        scale=scale * size_to_scale(normalized_size),
        quantity=max(quantity, 1),
        blade_length=blade_length,
        blade_width=blade_width,
        guard_width=guard_width,
        handle_length=handle_length,
        blade_style=resolved_blade_style,
        guard_style=resolved_guard_style,
        handle_style=resolved_handle_style,
        pommel_style=resolved_pommel_style,
        blade_material=blade_material.strip().lower(),
        guard_material=guard_material.strip().lower(),
        handle_material=handle_material.strip().lower(),
        pommel_material=pommel_material.strip().lower(),
        blade_attachment=blade_attachment.strip().lower(),
        guard_attachment=guard_attachment.strip().lower(),
        handle_attachment=handle_attachment.strip().lower(),
        pommel_attachment=pommel_attachment.strip().lower(),
        blade_pattern=blade_pattern.strip().lower(),
        handle_pattern=handle_pattern.strip().lower(),
        engraving=engraving.strip().lower(),
        gemstone=gemstone.strip().lower(),
    )

def asset_request_to_weapon_blueprint(
    asset_request,
) -> WeaponBlueprint:
    """Convert an existing sword AssetRequest into a WeaponBlueprint."""

    object_type = getattr(
        asset_request,
        "object_type",
        "",
    ).strip().lower()

    if object_type != "sword":
        raise ValueError(
            "Only sword AssetRequests can become WeaponBlueprints."
        )

    return create_weapon_blueprint(
        style=getattr(
            asset_request,
            "style",
            "sword",
        ),
        material=getattr(
            asset_request,
            "material",
            "iron",
        ),
        condition=getattr(
            asset_request,
            "condition",
            "clean",
        ),
        size=getattr(
            asset_request,
            "size",
            "normal",
        ),
        scale=getattr(
            asset_request,
            "scale",
            1.0,
        ),
        quantity=getattr(
            asset_request,
            "quantity",
            1,
        ),
        blade_length=getattr(
            asset_request,
            "blade_length",
            1.0,
        ),
        blade_width=getattr(
            asset_request,
            "blade_width",
            1.0,
        ),
        guard_width=getattr(
            asset_request,
            "guard_width",
            1.0,
        ),
        handle_length=getattr(
            asset_request,
            "handle_length",
            1.0,
        ),
        blade_style=getattr(
            asset_request,
            "blade_style",
            "automatic",
        ),
        guard_style=getattr(
            asset_request,
            "guard_style",
            "automatic",
        ),
        handle_style=getattr(
            asset_request,
            "handle_style",
            "automatic",
        ),
        pommel_style=getattr(
            asset_request,
            "pommel_style",
            "automatic",
        ),
        blade_material=getattr(
            asset_request,
            "blade_material",
            "automatic",
        ),
        guard_material=getattr(
            asset_request,
            "guard_material",
            "automatic",
        ),
        handle_material=getattr(
            asset_request,
            "handle_material",
            "automatic",
        ),
        pommel_material=getattr(
            asset_request,
            "pommel_material",
            "automatic",
        ),
        blade_attachment=getattr(
            asset_request,
            "blade_attachment",
            "none",
        ),
        guard_attachment=getattr(
            asset_request,
            "guard_attachment",
            "none",
        ),
        handle_attachment=getattr(
            asset_request,
            "handle_attachment",
            "none",
        ),
        pommel_attachment=getattr(
            asset_request,
            "pommel_attachment",
            "none",
        ),
        blade_pattern=getattr(
            asset_request,
            "blade_pattern",
            "none",
        ),
        handle_pattern=getattr(
            asset_request,
            "handle_pattern",
            "none",
        ),
        engraving=getattr(
            asset_request,
            "engraving",
            "none",
        ),
        gemstone=getattr(
            asset_request,
            "gemstone",
            "none",
        ),
    )

@dataclass
class TreeBlueprint:
    """Fully describes one procedural tree."""

    species: str = "pine"
    size: str = "normal"
    condition: str = "healthy"

    trunk_height: float = 2.5
    trunk_radius: float = 0.2

    lower_canopy_radius: float = 1.2
    lower_canopy_height: float = 2.0

    upper_canopy_radius: float = 0.8
    upper_canopy_height: float = 1.5

    trunk_sides: int = 10
    canopy_sections: int = 16

    bend: float = 0.0
    leaf_density: float = 1.0

  