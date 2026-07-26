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

    if contains_word(text, "dagger") or contains_word(text, "daggers"):
        return "dagger"

    if (
        contains_word(text, "greatsword")
        or contains_word(text, "greatswords")
    ):
        return "greatsword"

    return "sword"

def parse_prompt(prompt: str) -> list[AssetRequest]:
    """Convert the prompt into structured asset requests."""

    asset_requests: list[AssetRequest] = []

    for section in split_prompt(prompt):
        object_type = detect_object_type(section)

        print("SECTION:", section)
        print("OBJECT:", object_type)

        if object_type is None:
            continue

        asset_requests.append(
            AssetRequest(
                object_type=object_type,
                scale=detect_scale(section),
                material=detect_material(section),
                quantity=detect_quantity(section),
                style=detect_weapon_style(section),
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