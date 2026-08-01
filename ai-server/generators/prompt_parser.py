import re
from dataclasses import dataclass

from generators.attributes import (
    ATTRIBUTE_ALIASES,
    get_registered_values,
    normalize_attribute,
)
from generators.attribute_parser import parse_attributes


OBJECT_SYNONYMS = {
    "sword": (
        "sword",
        "swords",
        "blade",
        "blades",
        "longsword",
        "longswords",
        "broadsword",
        "broadswords",
        "weapon",
        "weapons",
        "dagger",
        "daggers",
        "greatsword",
        "greatswords",
    ),
    "shield": (
        "shield",
        "shields",
    ),
    "tree": (
        "tree",
        "trees",
        "pine",
        "pines",
        "oak",
        "oaks",
        "sapling",
        "saplings",
    ),
    "cube": (
        "cube",
        "cubes",
        "box",
        "boxes",
        "block",
        "blocks",
    ),
    "sphere": (
        "sphere",
        "spheres",
        "ball",
        "balls",
        "orb",
        "orbs",
        "globe",
        "globes",
    ),
    
}


@dataclass
class AssetRequest:
    """Structured instructions for one requested asset."""

    object_type: str
    scale: float = 1.0
    material: str = "iron"
    quantity: int = 1

    style: str = "sword"
    blade_length: float = 1.0
    blade_width: float = 1.0
    guard_width: float = 1.0
    handle_length: float = 1.0

    condition: str = "clean"
    shield_style: str = "round"
    axe_style: str = "axe"

    gemstone: str = "none"

def contains_word(text: str, word: str) -> bool:
    pattern = rf"\b{re.escape(word)}\b"
    return re.search(
        pattern,
        text,
        flags=re.IGNORECASE,
    ) is not None

def detect_scale(text: str) -> float:
    if contains_word(text, "tiny"):
        return 0.4

    if contains_word(text, "small"):
        return 0.65

    if contains_word(text, "giant") or contains_word(text, "huge"):
        return 2.0

    if contains_word(text, "large") or contains_word(text, "big"):
        return 1.5

    return 1.0


def detect_material(text: str) -> str:
    """Detect and normalize the requested material."""

    normalized_text = text.strip().lower()

    material_aliases = ATTRIBUTE_ALIASES.get(
        "material",
        {},
    )

    # Check longer aliases first, such as "black glass".
    sorted_aliases = sorted(
        material_aliases.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    )

    for alias, registered_material in sorted_aliases:
        if alias in normalized_text:
            return normalize_attribute(
                category="material",
                value=registered_material,
            )

    for material in get_registered_values("material"):
        if contains_word(normalized_text, material):
            return normalize_attribute(
                category="material",
                value=material,
            )

    return "iron"

def detect_quantity(prompt: str) -> int:
    """Detect how many objects the user wants."""

    words = prompt.lower().split()

    for word in words:
        if word.isdigit():
            return max(1, int(word))

    return 1


def detect_object_type(text: str) -> str | None:
    """Detect which supported object the text describes."""

    text_lower = text.lower()

    weapon_words = (
    "sword",
    "swords",
    "blade",
    "blades",
    "longsword",
    "longswords",
    "shortsword",
    "shortswords",
    "broadsword",
    "broadswords",
    "greatsword",
    "greatswords",
    "katana",
    "katanas",
    "rapier",
    "rapiers",
    "dagger",
    "daggers",
    "weapon",
    "weapons",
)
    weapon_words = (
    "sword",
    "swords",
    "blade",
    "blades",
    "longsword",
    "longswords",
    "shortsword",
    "shortswords",
    "broadsword",
    "broadswords",
    "greatsword",
    "greatswords",
    "katana",
    "katanas",
    "rapier",
    "rapiers",
    "dagger",
    "daggers",
    "weapon",
    "weapons",
)

    axe_words = (
        "axe",
        "axes",
        "hatchet",
        "hatchets",
        "battleaxe",
        "battleaxes",
    )

    shield_words = (
        "shield",
        "shields",
        "buckler",
        "bucklers",
    )

    tree_words = (
        "tree",
        "trees",
        "pine",
        "pines",
        "oak",
        "oaks",
        "sapling",
        "saplings",
    )

    tree_words = (
        "tree",
        "trees",
        "pine",
        "pines",
        "oak",
        "oaks",
        "sapling",
        "saplings",
    )

    cube_words = (
        "cube",
        "cubes",
        "box",
        "boxes",
        "block",
        "blocks",
    )

    sphere_words = (
        "sphere",
        "spheres",
        "ball",
        "balls",
        "orb",
        "orbs",
        "globe",
        "globes",
    )

    if any(word in text_lower for word in axe_words):
        return "axe"

    if any(word in text_lower for word in weapon_words):
        return "sword"

    if any(word in text_lower for word in shield_words):
        return "shield"

    if any(word in text_lower for word in tree_words):
        return "tree"

    if any(word in text_lower for word in cube_words):
        return "cube"

    if any(word in text_lower for word in sphere_words):
        return "sphere"

    return None

def split_prompt(prompt: str) -> list[str]:
    sections = re.split(
        r",|\band\b",
        prompt.lower(),
        flags=re.IGNORECASE,
    )

    return [
        section.strip()
        for section in sections
        if section.strip()
    ]

def detect_weapon_style(text: str) -> str:
    """Detect which sword-family style was requested."""

    if (
        contains_word(text, "dagger")
        or contains_word(text, "daggers")
    ):
        return "dagger"

    if (
        contains_word(text, "shortsword")
        or contains_word(text, "shortswords")
        or (
            contains_word(text, "short")
            and contains_word(text, "sword")
        )
    ):
        return "shortsword"

    if (
        contains_word(text, "greatsword")
        or contains_word(text, "greatswords")
        or (
            contains_word(text, "great")
            and contains_word(text, "sword")
        )
    ):
        return "greatsword"

    if (
        contains_word(text, "broadsword")
        or contains_word(text, "broadswords")
        or (
            contains_word(text, "broad")
            and contains_word(text, "sword")
        )
    ):
        return "broadsword"

    if (
        contains_word(text, "longsword")
        or contains_word(text, "longswords")
        or (
            contains_word(text, "long")
            and contains_word(text, "sword")
        )
    ):
        return "longsword"

    if (
        contains_word(text, "katana")
        or contains_word(text, "katanas")
    ):
        return "katana"

    if (
        contains_word(text, "rapier")
        or contains_word(text, "rapiers")
    ):
        return "rapier"

    return "sword"

def detect_blade_length(text: str) -> float:
    """Detect blade-length adjectives."""

    if contains_word(text, "short"):
        return 0.70

    if contains_word(text, "long"):
        return 1.30

    return 1.0

def detect_blade_width(text: str) -> float:
    """Detect blade width."""

    if contains_word(text, "thin"):
        return 0.70

    if contains_word(text, "narrow"):
        return 0.80

    if contains_word(text, "wide"):
        return 1.30

    if contains_word(text, "fat"):
        return 1.45

    return 1.0

def detect_condition(text: str) -> str:
    """Detect and normalize the requested object condition."""

    normalized_text = text.strip().lower()

    condition_aliases = ATTRIBUTE_ALIASES.get(
        "condition",
        {},
    )

    sorted_aliases = sorted(
        condition_aliases.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    )

    for alias, registered_condition in sorted_aliases:
        if alias in normalized_text:
            return normalize_attribute(
                category="condition",
                value=registered_condition,
            )

    for condition in get_registered_values("condition"):
        if contains_word(normalized_text, condition):
            return normalize_attribute(
                category="condition",
                value=condition,
            )

    return "clean"

def detect_shield_style(text: str) -> str:
    """Detect the requested shield style."""

    if contains_word(text, "tower"):
        return "tower"

    if contains_word(text, "kite"):
        return "kite"

    if (
        contains_word(text, "buckler")
        or contains_word(text, "bucklers")
    ):
        return "buckler"

    return "round"

def detect_axe_style(text: str) -> str:
    """Detect the requested axe style."""

    if (
        contains_word(text, "double")
        or contains_word(text, "doubleaxe")
        or contains_word(text, "doubleaxes")
    ):
        return "double"

    if (
        contains_word(text, "battleaxe")
        or contains_word(text, "battleaxes")
        or (
            contains_word(text, "battle")
            and contains_word(text, "axe")
        )
    ):
        return "battle"

    if (
        contains_word(text, "hatchet")
        or contains_word(text, "hatchets")
    ):
        return "hatchet"

    return "axe"

def parse_prompt(prompt: str) -> list[AssetRequest]:
    """Convert the prompt into structured asset requests."""

    asset_requests: list[AssetRequest] = []

    for section in split_prompt(prompt):
        object_type = detect_object_type(section)

        if object_type is None:
            continue

        attributes = parse_attributes(section)

        if object_type == "sword":
            material = attributes.material
            condition = attributes.condition
            style = attributes.weapon_style
            gemstone = attributes.gemstone

        else:
            material = detect_material(section)
            condition = detect_condition(section)
            style = detect_weapon_style(section)
            gemstone = "none"

        asset_requests.append(
            AssetRequest(
                object_type=object_type,
                scale=detect_scale(section),
                material=material,
                quantity=detect_quantity(section),
                style=style,
                blade_length=detect_blade_length(section),
                blade_width=detect_blade_width(section),
                condition=condition,
                shield_style=detect_shield_style(section),
                axe_style=detect_axe_style(section),
                gemstone=gemstone,
            )
        )

    if not asset_requests:
        raise ValueError(
            "Genesis did not recognize any supported objects. "
            "Try sword, axe, shield, tree, cube, or sphere."
        )

    return asset_requests