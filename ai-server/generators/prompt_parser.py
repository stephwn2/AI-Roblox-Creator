import re
from dataclasses import dataclass


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
    object_type: str
    scale: float = 1.0
    material: str = "iron"
    quantity: int = 1
    style: str = "sword"
    blade_length: float = 1.0
    blade_width: float = 1.0
    condition: str = "clean"

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
    if contains_word(text, "gold") or contains_word(text, "golden"):
        return "gold"

    if contains_word(text, "wood") or contains_word(text, "wooden"):
        return "wood"

    if any(
        contains_word(text, word)
        for word in ("iron", "steel", "metal")
    ):
        return "iron"

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
        "broadsword",
        "broadswords",
        "dagger",
        "daggers",
        "greatsword",
        "greatswords",
        "weapon",
        "weapons",
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

    if any(word in text_lower for word in weapon_words):
        return "sword"

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
    """Detect which sword-family style the user requested."""

    if (
        contains_word(text, "greatsword")
        or contains_word(text, "greatswords")
    ):
        return "greatsword"

    if (
        contains_word(text, "broadsword")
        or contains_word(text, "broadswords")
    ):
        return "broadsword"

    if (
        contains_word(text, "dagger")
        or contains_word(text, "daggers")
    ):
        return "dagger"

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
    """Detect the object's surface condition."""

    if contains_word(text, "rusty") or contains_word(text, "rusted"):
        return "rusty"

    return "clean"

def parse_prompt(prompt: str) -> list[AssetRequest]:
    """Convert the prompt into structured asset requests."""

    asset_requests: list[AssetRequest] = []

    for section in split_prompt(prompt):
        object_type = detect_object_type(section)


        if object_type is None:
            continue

        asset_requests.append(
            AssetRequest(
                object_type=object_type,
                scale=detect_scale(section),
                material=detect_material(section),
                quantity=detect_quantity(section),
                style=detect_weapon_style(section),
                blade_length=detect_blade_length(section),
                blade_width=detect_blade_width(section),
                condition=detect_condition(section),
)
        )

    if not asset_requests:
        raise ValueError(
            "Genesis did not recognize any supported objects. "
            "Try sword, tree, cube, or sphere."
        )

    return asset_requests
    if not asset_requests:
        raise ValueError(
            "Genesis did not recognize any supported objects. "
            "Try sword, tree, cube, or sphere."
        )

    return asset_requests