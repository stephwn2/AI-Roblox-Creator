import trimesh

from generators.weapon_parts.blades.broadsword import (
    create_broadsword_blade,
)
from generators.weapon_parts.blades.dagger import (
    create_dagger_blade,
)
from generators.weapon_parts.blades.greatsword import (
    create_greatsword_blade,
)
from generators.weapon_parts.blades.katana import (
    create_katana_blade,
)
from generators.weapon_parts.blades.longsword import (
    create_longsword_blade,
)
from generators.weapon_parts.blades.rapier import (
    create_rapier_blade,
)
from generators.weapon_parts.blades.shortsword import (
    create_shortsword_blade,
)
from generators.weapon_parts.blades.sword import (
    create_sword_blade,
)


def create_blade(
    length_multiplier: float,
    width_multiplier: float,
    color: list[int],
    style: str = "sword",
) -> trimesh.Trimesh:
    """Route the requested style to its blade generator."""

    blade_generators = {
        "sword": create_sword_blade,
        "dagger": create_dagger_blade,
        "shortsword": create_shortsword_blade,
        "longsword": create_longsword_blade,
        "broadsword": create_broadsword_blade,
        "greatsword": create_greatsword_blade,
        "katana": create_katana_blade,
        "rapier": create_rapier_blade,
    }

    generator = blade_generators.get(
        style,
        create_sword_blade,
    )

    return generator(
        length_multiplier=length_multiplier,
        width_multiplier=width_multiplier,
        color=color,
    )