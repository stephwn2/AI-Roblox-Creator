from typing import TypeAlias

from generators.weapon_parts.condition import (
    apply_condition_to_colors,
)


Color: TypeAlias = list[int]
MaterialPalette: TypeAlias = dict[str, Color]


MATERIAL_PALETTES: dict[str, MaterialPalette] = {
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

    "steel": {
        "blade": [205, 215, 225, 255],
        "guard": [145, 155, 170, 255],
        "handle": [68, 40, 24, 255],
        "pommel": [145, 155, 170, 255],
    },

    "gold": {
        "blade": [212, 170, 45, 255],
        "guard": [235, 195, 65, 255],
        "handle": [92, 48, 24, 255],
        "pommel": [235, 195, 65, 255],
    },

    "obsidian": {
        "blade": [28, 25, 35, 255],
        "guard": [50, 42, 62, 255],
        "handle": [35, 24, 28, 255],
        "pommel": [50, 42, 62, 255],
    },

    "crystal": {
        "blade": [125, 220, 245, 210],
        "guard": [85, 165, 215, 255],
        "handle": [65, 75, 105, 255],
        "pommel": [110, 195, 235, 255],
    },

    "bone": {
        "blade": [220, 210, 180, 255],
        "guard": [190, 180, 150, 255],
        "handle": [110, 75, 45, 255],
        "pommel": [200, 190, 160, 255],
    },

    "mithril": {
        "blade": [195, 225, 235, 255],
        "guard": [150, 195, 215, 255],
        "handle": [60, 55, 75, 255],
        "pommel": [160, 205, 225, 255],
    },
}


def get_material_palette(
    material: str,
    condition: str = "clean",
) -> MaterialPalette:
    """Return weapon-part colors for a material and condition."""

    normalized_material = material.strip().lower()

    base_palette = MATERIAL_PALETTES.get(
        normalized_material,
        MATERIAL_PALETTES["iron"],
    )

    colors = {
        part_name: part_color.copy()
        for part_name, part_color in base_palette.items()
    }

    return apply_condition_to_colors(
        colors=colors,
        condition=condition,
    )