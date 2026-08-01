import re
from dataclasses import dataclass

from generators.attributes import (
    ATTRIBUTE_ALIASES,
    get_registered_values,
    normalize_attribute,
)


@dataclass
class ParsedAttributes:
    """Structured attributes extracted from a text prompt."""

    material: str = "iron"
    condition: str = "clean"
    size: str = "normal"
    weapon_style: str = "sword"
    gemstone: str = "none"

def contains_word(
    text: str,
    word: str,
) -> bool:
    """Return whether a complete word or phrase exists in the text."""

    pattern = rf"\b{re.escape(word)}\b"

    return re.search(
        pattern,
        text,
        flags=re.IGNORECASE,
    ) is not None


def detect_attribute(
    text: str,
    category: str,
    default: str,
) -> str:
    """Detect one registered attribute category from a prompt."""

    normalized_text = text.strip().lower()

    aliases = ATTRIBUTE_ALIASES.get(
        category,
        {},
    )

    sorted_aliases = sorted(
        aliases.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    )

    for alias, registered_value in sorted_aliases:
        if contains_word(normalized_text, alias):
            return normalize_attribute(
                category=category,
                value=registered_value,
            )

    registered_values = sorted(
        get_registered_values(category),
        key=len,
        reverse=True,
    )

    for registered_value in registered_values:
        if contains_word(
            normalized_text,
            registered_value,
        ):
            return normalize_attribute(
                category=category,
                value=registered_value,
            )

    return default


def detect_material_attribute(text: str) -> str:
    """Detect the requested material."""

    return detect_attribute(
        text=text,
        category="material",
        default="iron",
    )


def detect_condition_attribute(text: str) -> str:
    """Detect the requested condition."""

    return detect_attribute(
        text=text,
        category="condition",
        default="clean",
    )


def detect_size_attribute(text: str) -> str:
    """Detect the requested object size."""

    return detect_attribute(
        text=text,
        category="size",
        default="normal",
    )

def detect_gemstone_attribute(text: str) -> str:
    """Detect the requested gemstone."""

    return detect_attribute(
        text=text,
        category="gemstone",
        default="none",
    )


def detect_weapon_style_attribute(text: str) -> str:
    """Detect the requested sword-family style."""

    return detect_attribute(
        text=text,
        category="weapon_style",
        default="sword",
    )


def parse_attributes(text: str) -> ParsedAttributes:
    """Extract all currently supported attributes."""

    normalized_text = text.strip().lower()

    return ParsedAttributes(
        material=detect_material_attribute(normalized_text),
        condition=detect_condition_attribute(normalized_text),
        size=detect_size_attribute(normalized_text),
        weapon_style=detect_weapon_style_attribute(
            normalized_text,
        ),
        gemstone=detect_gemstone_attribute(
            normalized_text,
        ),
    )
