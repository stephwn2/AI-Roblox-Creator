import trimesh

from generators.blueprints import TreeBlueprint
from generators.tree_blueprint_builder import create_tree_blueprint


def build_tree_from_blueprint(
    blueprint: TreeBlueprint,
    scale: float = 1.0,
) -> trimesh.Scene:
    """Build tree geometry from a completed TreeBlueprint."""

    trunk_color = [110, 72, 38, 255]
    lower_leaf_color = [42, 110, 52, 255]
    upper_leaf_color = [52, 130, 62, 255]

    if blueprint.condition == "dead":
        trunk_color = [92, 76, 58, 255]
        lower_leaf_color = [110, 95, 70, 255]
        upper_leaf_color = [130, 110, 85, 255]

    elif blueprint.condition == "snowy":
        trunk_color = [85, 66, 48, 255]
        lower_leaf_color = [225, 235, 238, 255]
        upper_leaf_color = [245, 248, 250, 255]

    elif blueprint.condition == "ancient":
        trunk_color = [82, 55, 34, 255]
        lower_leaf_color = [35, 92, 43, 255]
        upper_leaf_color = [45, 108, 52, 255]

    elif blueprint.condition == "lush":
        lower_leaf_color = [32, 125, 48, 255]
        upper_leaf_color = [45, 155, 62, 255]

    trunk = trimesh.creation.cylinder(
        radius=blueprint.trunk_radius,
        height=blueprint.trunk_height,
        sections=blueprint.trunk_sides,
    )

    trunk.visual.face_colors = trunk_color

    trunk.apply_translation(
        (
            blueprint.bend,
            0.0,
            blueprint.trunk_height / 2,
        )
    )

    lower_canopy = trimesh.creation.cone(
        radius=blueprint.lower_canopy_radius,
        height=blueprint.lower_canopy_height,
        sections=blueprint.canopy_sections,
    )

    lower_canopy.visual.face_colors = lower_leaf_color

    lower_canopy.apply_translation(
        (
            blueprint.bend,
            0.0,
            blueprint.trunk_height * 0.72,
        )
    )

    upper_canopy = trimesh.creation.cone(
        radius=blueprint.upper_canopy_radius,
        height=blueprint.upper_canopy_height,
        sections=blueprint.canopy_sections,
    )

    upper_canopy.visual.face_colors = upper_leaf_color

    upper_canopy.apply_translation(
        (
            blueprint.bend * 1.30,
            0.0,
            blueprint.trunk_height * 1.12,
        )
    )

    scene = trimesh.Scene()

    scene.add_geometry(
        trunk,
        node_name="Trunk",
    )

    if blueprint.leaf_density > 0.10:
        scene.add_geometry(
            lower_canopy,
            node_name="LowerCanopy",
        )

    if blueprint.leaf_density > 0.30:
        scene.add_geometry(
            upper_canopy,
            node_name="UpperCanopy",
        )

    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)

    return scene


def create_tree(
    scale: float = 1.0,
    variation: bool = True,
    tree_style: str = "pine",
    condition: str = "healthy",
    size: str = "normal",
) -> trimesh.Scene:
    """Create a procedural tree through the blueprint pipeline."""

    blueprint = create_tree_blueprint(
        species=tree_style,
        size=size,
        condition=condition,
        variation=variation,
    )

    return build_tree_from_blueprint(
        blueprint=blueprint,
        scale=scale,
    )