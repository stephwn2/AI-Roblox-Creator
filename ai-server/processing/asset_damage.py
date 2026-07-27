"""
Damage processing for generated assets.

This module will eventually contain all visual damage effects such as:

- Rust
- Cracks
- Chips
- Broken pieces
- Moss
- Blood
- Dirt
- Age
"""

import trimesh

def apply_broken_blade_damage(
    scene: trimesh.Scene,
    damage_amount: float = 0.45,
) -> trimesh.Scene:
    """Shorten and slightly bend blade geometry to simulate damage."""

    damaged_scene = scene.copy()

    damage_amount = max(0.0, min(damage_amount, 0.8))
    length_multiplier = 1.0 - damage_amount

    for geometry_name, geometry in damaged_scene.geometry.items():
        if "blade" not in geometry_name.lower():
            continue

        vertices = geometry.vertices.copy()

        minimum_z = vertices[:, 2].min()
        maximum_z = vertices[:, 2].max()
        blade_height = maximum_z - minimum_z

        if blade_height <= 0:
            continue

        normalized_height = (
            vertices[:, 2] - minimum_z
        ) / blade_height

        # Shorten the blade.
        vertices[:, 2] = (
            minimum_z
            + normalized_height
            * blade_height
            * length_multiplier
        )

        # Bend the upper half slightly sideways.
        bend_amount = 0.12 * damage_amount
        vertices[:, 0] += (
            normalized_height ** 2
        ) * bend_amount

        geometry.vertices = vertices

    return damaged_scene