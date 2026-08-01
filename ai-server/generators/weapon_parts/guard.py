import trimesh

from generators.weapon_parts.guards.cross_guard import (
    create_cross_guard,
)
from generators.weapon_parts.guards.great_guard import (
    create_great_guard,
)
from generators.weapon_parts.guards.rapier_guard import (
    create_rapier_guard,
)
from generators.weapon_parts.guards.round_guard import (
    create_round_guard,
)
from generators.weapon_parts.guards.tsuba_guard import (
    create_tsuba_guard,
)


def create_guard(
    width_multiplier: float,
    color: list[int],
    style: str = "cross",
) -> trimesh.Trimesh:
    """Route an explicit guard style to its generator."""

    normalized_style = style.strip().lower()

    guard_generators = {
        "cross": create_cross_guard,
        "round": create_round_guard,
        "tsuba": create_tsuba_guard,
        "rapier": create_rapier_guard,
        "great": create_great_guard,

        # Compatibility with older weapon-family values.
        "sword": create_cross_guard,
        "dagger": create_cross_guard,
        "shortsword": create_cross_guard,
        "longsword": create_cross_guard,
        "broadsword": create_cross_guard,
        "katana": create_tsuba_guard,
        "greatsword": create_great_guard,
    }

    generator = guard_generators.get(
        normalized_style,
        create_cross_guard,
    )

    return generator(
        width_multiplier=width_multiplier,
        color=color,
    )