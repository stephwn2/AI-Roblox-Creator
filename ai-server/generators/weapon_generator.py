import random
import trimesh

from generators.weapon_parts.blade import create_blade
from generators.weapon_parts.guard import create_guard
from generators.weapon_parts.handle import create_handle
from generators.weapon_parts.pommel import create_pommel
from generators.weapon_parts.material import get_material_palette
from generators.weapon_parts.condition import (
    get_blade_condition_multiplier,
)

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

    "shortsword": {
    "blade_length": 0.80,
    "blade_width": 0.90,
    "guard_width": 0.90,
    "handle_length": 0.85,
},

"longsword": {
    "blade_length": 1.30,
    "blade_width": 1.00,
    "guard_width": 1.05,
    "handle_length": 1.35,
},

"katana": {
    "blade_length": 1.20,
    "blade_width": 0.85,
    "guard_width": 0.80,
    "handle_length": 1.40,
},

"rapier": {
    "blade_length": 1.35,
    "blade_width": 0.55,
    "guard_width": 1.15,
    "handle_length": 1.05,
},
},
}

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
) -> trimesh.Scene:
    """Create a modular low-poly sword."""

    colors = get_material_palette(
        material=material,
        condition=condition,
    )

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

    blade_condition_multiplier = get_blade_condition_multiplier(
        condition=condition,
    )

    blade_length_multiplier = (
        style_settings["blade_length"]
        * variation_blade_length
        * blade_length
        * blade_condition_multiplier
    )

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
        style=style,
    )

    guard = create_guard(
        width_multiplier=guard_width_multiplier,
        color=colors["guard"],
        style=style,
    )

    handle = create_handle(
        length_multiplier=handle_length_multiplier,
        color=colors["handle"],
        style=style,
    )

    pommel = create_pommel(
        size_multiplier=pommel_size_multiplier,
        color=colors["pommel"],
        style=style,
    )

    scene = trimesh.Scene()

    scene.add_geometry(
        blade,
        node_name="Blade",
    )

    scene.add_geometry(
        guard,
        node_name="Guard",
    )

    scene.add_geometry(
        handle,
        node_name="Handle",
    )

    scene.add_geometry(
        pommel,
        node_name="Pommel",
    )

    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)

    return scene