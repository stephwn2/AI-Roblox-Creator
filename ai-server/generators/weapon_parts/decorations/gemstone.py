import trimesh

from generators.weapon_parts.attachment_sockets import (
    AttachmentSocket,
)


GEMSTONE_COLORS: dict[str, list[int]] = {
    "ruby": [190, 25, 45, 255],
    "sapphire": [35, 85, 200, 255],
    "emerald": [25, 165, 90, 255],
    "amethyst": [125, 65, 180, 255],
    "diamond": [210, 240, 255, 220],
    "onyx": [30, 30, 38, 255],
}


def create_pommel_gemstone(
    gemstone: str,
    socket: AttachmentSocket,
) -> trimesh.Trimesh:
    """Create a gemstone using a pommel attachment socket."""

    normalized_gemstone = gemstone.strip().lower()

    color = GEMSTONE_COLORS.get(
        normalized_gemstone,
        GEMSTONE_COLORS["ruby"],
    )

    gem = trimesh.creation.icosphere(
        subdivisions=2,
        radius=0.075 * socket.scale,
    )

    gem.apply_scale(
        (
            0.75,
            0.45,
            0.75,
        )
    )

    gem.visual.face_colors = color
    gem.apply_translation(socket.position)

    return gem