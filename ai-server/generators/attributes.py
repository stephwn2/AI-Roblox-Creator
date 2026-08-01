from typing import Final


ATTRIBUTE_REGISTRY: Final[dict[str, tuple[str, ...]]] = {
    "material": (
        "wood",
        "iron",
        "steel",
        "gold",
        "obsidian",
        "crystal",
        "bone",
        "mithril",
    ),

    "condition": (
        "clean",
        "rusty",
        "old",
        "ancient",
        "aged",
        "enchanted",
        "magic",
        "magical",
        "burned",
        "charred",
        "broken",
        "snapped",
        "chipped",
        "damaged",
    ),

    "size": (
        "tiny",
        "small",
        "normal",
        "large",
        "big",
        "giant",
        "massive",
        "huge",
    ),

    "weapon_style": (
        "sword",
        "dagger",
        "shortsword",
        "longsword",
        "broadsword",
        "greatsword",
        "katana",
        "rapier",
    ),

    "shield_style": (
        "round",
        "buckler",
        "kite",
        "tower",
    ),

    "axe_style": (
        "axe",
        "hatchet",
        "battle",
        "double",
        "great",
    ),
}


ATTRIBUTE_ALIASES: Final[dict[str, dict[str, str]]] = {
    "material": {
        "wooden": "wood",
        "metal": "iron",
        "silver": "steel",
        "golden": "gold",
        "black glass": "obsidian",
    },

    "condition": {
        "rusted": "rusty",
        "weathered": "old",
        "antique": "ancient",
        "scorched": "burned",
        "shattered": "broken",
        "cracked": "damaged",
    },

    "size": {
        "little": "small",
        "short": "small",
        "big": "large",
        "huge": "massive",
        "gigantic": "massive",
    },

    "weapon_style": {
        "great sword": "greatsword",
        "long sword": "longsword",
        "short sword": "shortsword",
        "broad sword": "broadsword",
    },
}


def normalize_attribute(
    category: str,
    value: str,
) -> str:
    """Normalize an attribute value using aliases."""

    normalized_category = category.strip().lower()
    normalized_value = value.strip().lower()

    aliases = ATTRIBUTE_ALIASES.get(
        normalized_category,
        {},
    )

    return aliases.get(
        normalized_value,
        normalized_value,
    )


def get_registered_values(
    category: str,
) -> tuple[str, ...]:
    """Return every registered value for an attribute category."""

    normalized_category = category.strip().lower()

    return ATTRIBUTE_REGISTRY.get(
        normalized_category,
        (),
    )


def is_registered_attribute(
    category: str,
    value: str,
) -> bool:
    """Return whether an attribute value is registered."""

    normalized_value = normalize_attribute(
        category=category,
        value=value,
    )

    return normalized_value in get_registered_values(
        category=category,
    )