import trimesh

from generators.nature_generator import create_tree
from generators.prompt_parser import AssetRequest, parse_prompt
from generators.weapon_generator import create_sword
from generators.shield_generator import create_shield
from generators.axe_generator import create_axe
from generators.blueprints import (
    asset_request_to_weapon_blueprint,
)

def create_sword_scene(asset):
    """Convert a sword request into a blueprint and build it."""

    blueprint = asset_request_to_weapon_blueprint(asset)

    return create_sword(
        scale=blueprint.scale,
        material=blueprint.material,
        style=blueprint.style,
        blade_style=blueprint.blade_style,
        guard_style=blueprint.guard_style,
        handle_style=blueprint.handle_style,
        pommel_style=blueprint.pommel_style,
        blade_length=blueprint.blade_length,
        blade_width=blueprint.blade_width,
        guard_width=blueprint.guard_width,
        handle_length=blueprint.handle_length,
        condition=blueprint.condition,
        gemstone=blueprint.gemstone,
        engraving=blueprint.engraving,
        blade_attachment=blueprint.blade_attachment,
        guard_attachment=blueprint.guard_attachment,
        handle_attachment=blueprint.handle_attachment,
        pommel_attachment=blueprint.pommel_attachment,
    )

def create_object_scene(asset: AssetRequest) -> trimesh.Scene:
    """Generate one object using its parsed instructions."""

    if asset.object_type == "sword":
        return create_sword_scene(asset)

    if asset.object_type == "axe":
            return create_axe(
                scale=asset.scale,
                material=asset.material,
                style=asset.axe_style,
            )
    if asset.object_type == "shield":
        return create_shield(
            scale=asset.scale,
            material=asset.material,
            style=asset.shield_style,
    )
    
    if asset.object_type == "tree":
        return create_tree(scale=asset.scale)

    if asset.object_type == "cube":
        cube = trimesh.creation.box(
            extents=(
                2 * asset.scale,
                2 * asset.scale,
                2 * asset.scale,
            ),
        )
        return trimesh.Scene(cube)

    if asset.object_type == "sphere":
        sphere = trimesh.creation.icosphere(
            subdivisions=3,
            radius=1.2 * asset.scale,
        )
        return trimesh.Scene(sphere)

    raise ValueError(
        f"Unsupported object type: {asset.object_type}"
    )


def route_prompt(prompt: str) -> trimesh.Scene:
    """Parse the prompt and generate every requested object."""

    asset_requests = parse_prompt(prompt)

    combined_scene = trimesh.Scene()
    x_cursor = 0.0
    gap = 2.0

    object_number = 0

    for asset in asset_requests:
        for copy_index in range(asset.quantity):
            object_scene = create_object_scene(asset)

            bounds = object_scene.bounds
            minimum_x = float(bounds[0][0])
            maximum_x = float(bounds[1][0])
            object_width = maximum_x - minimum_x

            x_offset = x_cursor - minimum_x

            for geometry_index, geometry in enumerate(
                object_scene.geometry.values()
            ):
                geometry_copy = geometry.copy()
                geometry_copy.apply_translation(
                    (x_offset, 0.0, 0.0)
                )

                unique_name = (
                    f"{asset.object_type}_"
                    f"{object_number}_"
                    f"{geometry_index}"
                )

                combined_scene.add_geometry(
                    geometry_copy,
                    node_name=unique_name,
                    geom_name=unique_name,
                )

            x_cursor += object_width + gap
            object_number += 1

    return combined_scene