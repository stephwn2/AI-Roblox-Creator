import trimesh

from generators.weapon_parts.pommels.flat_pommel import (
    create_flat_pommel,
)
from generators.weapon_parts.pommels.gem_pommel import (
    create_gem_pommel,
)
from generators.weapon_parts.pommels.heavy_pommel import (
    create_heavy_pommel,
)
from generators.weapon_parts.pommels.round_pommel import (
    create_round_pommel,
)


def create_pommel(
    size_multiplier: float,
    color: list[int],
    style: str = "sword",
) -> trimesh.Trimesh:
    """Route the requested weapon style to its pommel generator."""

    if style == "katana":
        return create_flat_pommel(
            size_multiplier=size_multiplier,
            color=color,
        )

    if style == "greatsword":
        return create_heavy_pommel(
            size_multiplier=size_multiplier,
            color=color,
        )

    if style == "rapier":
        return create_gem_pommel(
            size_multiplier=size_multiplier,
            color=color,
        )

    return create_round_pommel(
        size_multiplier=size_multiplier,
        color=color,
    )