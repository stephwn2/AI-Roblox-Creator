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
    style: str = "sword",
) -> trimesh.Trimesh:
    """Route the requested weapon style to its guard generator."""

    if style == "katana":
        return create_tsuba_guard(
            width_multiplier=width_multiplier,
            color=color,
        )

    if style == "rapier":
        return create_rapier_guard(
            width_multiplier=width_multiplier,
            color=color,
        )

    if style == "greatsword":
        return create_great_guard(
            width_multiplier=width_multiplier,
            color=color,
        )

    if style == "round":
        return create_round_guard(
            width_multiplier=width_multiplier,
            color=color,
        )

    return create_cross_guard(
        width_multiplier=width_multiplier,
        color=color,
    )