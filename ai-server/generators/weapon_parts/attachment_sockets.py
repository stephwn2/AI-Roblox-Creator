from dataclasses import dataclass


@dataclass(frozen=True)
class AttachmentSocket:
    """A named position and size for attaching a decoration."""

    position: tuple[float, float, float]
    scale: float = 1.0


POMMEL_GEMSTONE_SOCKETS: dict[str, AttachmentSocket] = {
    # Standard round pommel used by swords and longswords.
    "round": AttachmentSocket(
        position=(0.0, -0.205, -0.48),
        scale=1.05,
    ),

    # Thin katana end cap. Move the gemstone farther outward
    # so it does not disappear inside the flat pommel.
    "flat": AttachmentSocket(
        position=(0.0, -0.155, -0.48),
        scale=0.95,
    ),

    # Large greatsword pommel.
    "heavy": AttachmentSocket(
        position=(0.0, -0.225, -0.48),
        scale=1.20,
    ),

    # Faceted rapier pommel.
    "gem": AttachmentSocket(
        position=(0.0, -0.155, -0.48),
        scale=0.90,
    ),
}


def get_pommel_gemstone_socket(
    pommel_style: str,
) -> AttachmentSocket:
    """Return the correct gemstone socket for a pommel style."""

    normalized_style = pommel_style.strip().lower()

    compatibility_styles = {
        "sword": "round",
        "dagger": "round",
        "shortsword": "round",
        "longsword": "round",
        "broadsword": "round",
        "katana": "flat",
        "greatsword": "heavy",
        "rapier": "gem",
    }

    resolved_style = compatibility_styles.get(
        normalized_style,
        normalized_style,
    )

    return POMMEL_GEMSTONE_SOCKETS.get(
        resolved_style,
        POMMEL_GEMSTONE_SOCKETS["round"],
    )