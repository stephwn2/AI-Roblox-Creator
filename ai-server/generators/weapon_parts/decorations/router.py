import trimesh

from generators.weapon_parts.attachment_sockets import (
    get_pommel_gemstone_socket,
)
from generators.weapon_parts.decorations.gemstone import (
    create_pommel_gemstone,
)


def create_weapon_decorations(
    gemstone: str = "none",
    pommel_style: str = "round",
    engraving: str = "none",
    blade_attachment: str = "none",
    guard_attachment: str = "none",
    handle_attachment: str = "none",
    pommel_attachment: str = "none",
) -> list[tuple[str, trimesh.Trimesh]]:
    """Create all requested weapon decorations."""

    decorations: list[tuple[str, trimesh.Trimesh]] = []

    normalized_gemstone = gemstone.strip().lower()

    if normalized_gemstone not in {
        "",
        "none",
        "automatic",
    }:
        gemstone_socket = get_pommel_gemstone_socket(
            pommel_style=pommel_style,
        )

        gemstone_mesh = create_pommel_gemstone(
            gemstone=normalized_gemstone,
            socket=gemstone_socket,
        )

        decorations.append(
            (
                "PommelGemstone",
                gemstone_mesh,
            )
        )

    _ = (
        engraving,
        blade_attachment,
        guard_attachment,
        handle_attachment,
        pommel_attachment,
    )

    return decorations