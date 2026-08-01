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
    style: str = "sword",
) -> trimesh.Trimesh:
    """Route the requested style to its handle generator."""

    if style == "katana":
        return create_katana_handle(
            length_multiplier=length_multiplier,
            color=color,
        )

    if style == "rapier":
        return create_rapier_handle(
            length_multiplier=length_multiplier,
            color=color,
        )

    if style == "greatsword":
        return create_great_handle(
            length_multiplier=length_multiplier,
            color=color,
        )

    if style in {
        "longsword",
        "broadsword",
    }:
        return create_wrapped_handle(
            length_multiplier=length_multiplier,
            color=color,
        )

    return create_wood_handle(
        length_multiplier=length_multiplier,
        color=color,
    )