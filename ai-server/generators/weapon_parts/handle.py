import trimesh

from generators.weapon_parts.handles.great_handle import (
    create_great_handle,
)
from generators.weapon_parts.handles.katana_handle import (
    create_katana_handle,
)
from generators.weapon_parts.handles.rapier_handle import (
    create_rapier_handle,
)
from generators.weapon_parts.handles.wood_handle import (
    create_wood_handle,
)
from generators.weapon_parts.handles.wrapped_handle import (
    create_wrapped_handle,
)


def create_handle(
    length_multiplier: float,
    color: list[int],
    style: str = "wood",
) -> trimesh.Trimesh:
    """Route an explicit handle style to its generator."""

    normalized_style = style.strip().lower()

    handle_generators = {
        "wood": create_wood_handle,
        "wrapped": create_wrapped_handle,
        "katana": create_katana_handle,
        "great": create_great_handle,
        "rapier": create_rapier_handle,

        # Compatibility with older weapon-family values.
        "sword": create_wood_handle,
        "dagger": create_wood_handle,
        "shortsword": create_wood_handle,
        "longsword": create_wrapped_handle,
        "broadsword": create_wrapped_handle,
        "greatsword": create_great_handle,
    }

    generator = handle_generators.get(
        normalized_style,
        create_wood_handle,
    )

    return generator(
        length_multiplier=length_multiplier,
        color=color,
    )