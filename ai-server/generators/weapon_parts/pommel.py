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
    style: str = "round",
) -> trimesh.Trimesh:
    """Route an explicit pommel style to its generator."""

    normalized_style = style.strip().lower()

    pommel_generators = {
        "round": create_round_pommel,
        "flat": create_flat_pommel,
        "heavy": create_heavy_pommel,
        "gem": create_gem_pommel,

        # Compatibility with older weapon-family values.
        "sword": create_round_pommel,
        "dagger": create_round_pommel,
        "shortsword": create_round_pommel,
        "longsword": create_round_pommel,
        "broadsword": create_round_pommel,
        "katana": create_flat_pommel,
        "greatsword": create_heavy_pommel,
        "rapier": create_gem_pommel,
    }

    generator = pommel_generators.get(
        normalized_style,
        create_round_pommel,
    )

    return generator(
        size_multiplier=size_multiplier,
        color=color,
    )