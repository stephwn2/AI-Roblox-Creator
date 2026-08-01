import random

from generators.blueprints import TreeBlueprint
from generators.modifiers import get_asset_modifiers


def create_tree_blueprint(
    species: str = "pine",
    size: str = "normal",
    condition: str = "healthy",
    variation: bool = True,
) -> TreeBlueprint:
    """Create a complete procedural tree blueprint."""

    normalized_species = species.strip().lower()
    normalized_size = size.strip().lower()
    normalized_condition = condition.strip().lower()

    modifiers = get_asset_modifiers(
        size=normalized_size,
        condition=normalized_condition,
    )

    if variation:
        base_trunk_height = random.uniform(2.2, 3.2)
        base_trunk_radius = random.uniform(0.16, 0.24)

        base_lower_canopy_radius = random.uniform(0.90, 1.35)
        base_lower_canopy_height = random.uniform(1.60, 2.40)

        base_upper_canopy_radius = random.uniform(0.60, 1.00)
        base_upper_canopy_height = random.uniform(1.20, 1.90)

        trunk_sides = random.choice((8, 10, 12))
        canopy_sections = random.choice((12, 16, 20))

    else:
        base_trunk_height = 2.60
        base_trunk_radius = 0.20

        base_lower_canopy_radius = 1.20
        base_lower_canopy_height = 2.20

        base_upper_canopy_radius = 0.85
        base_upper_canopy_height = 1.80

        trunk_sides = 10
        canopy_sections = 16

    bend = modifiers.extras.get(
        "bend",
        0.0,
    )

    if bend > 0.0 and variation:
        bend *= random.choice((-1.0, 1.0))

    leaf_density = modifiers.extras.get(
        "leaf_density",
        1.0,
    )

    return TreeBlueprint(
        species=normalized_species,
        size=normalized_size,
        condition=normalized_condition,

        trunk_height=(
            base_trunk_height
            * modifiers.trunk_height
        ),
        trunk_radius=(
            base_trunk_radius
            * modifiers.trunk_radius
        ),

        lower_canopy_radius=(
            base_lower_canopy_radius
            * modifiers.canopy_radius
        ),
        lower_canopy_height=(
            base_lower_canopy_height
            * modifiers.canopy_height
        ),

        upper_canopy_radius=(
            base_upper_canopy_radius
            * modifiers.canopy_radius
        ),
        upper_canopy_height=(
            base_upper_canopy_height
            * modifiers.canopy_height
        ),

        trunk_sides=trunk_sides,
        canopy_sections=canopy_sections,

        bend=bend,
        leaf_density=leaf_density,
    )
