import trimesh

from generators.nature_generator import create_tree
from generators.weapon_generator import create_sword


OBJECT_SYNONYMS = {
    "sword": (
        "sword",
        "blade",
        "longsword",
        "broadsword",
        "weapon",
    ),
    "tree": (
        "tree",
        "pine",
        "oak",
        "sapling",
    ),
    "cube": (
        "cube",
        "box",
        "block",
    ),
    "sphere": (
        "sphere",
        "ball",
        "orb",
        "globe",
    ),
}


def detect_scale(prompt: str) -> float:
    """Read size words from a prompt and return a scale multiplier."""

    prompt_lower = prompt.lower()

    if "tiny" in prompt_lower:
        return 0.4

    if "small" in prompt_lower:
        return 0.65

    if "giant" in prompt_lower or "huge" in prompt_lower:
        return 2.0

    if "large" in prompt_lower or "big" in prompt_lower:
        return 1.5

    return 1.0


def detect_material(prompt: str) -> str:
    """Detect a basic material word in the prompt."""

    prompt_lower = prompt.lower()

    if any(word in prompt_lower for word in ("gold", "golden")):
        return "gold"

    if any(word in prompt_lower for word in ("wood", "wooden")):
        return "wood"

    if any(word in prompt_lower for word in ("iron", "steel", "metal")):
        return "iron"

    return "iron"


def detect_object_type(prompt: str) -> str:
    """Determine which supported object the prompt describes."""

    prompt_lower = prompt.lower()

    for object_type, words in OBJECT_SYNONYMS.items():
        if any(word in prompt_lower for word in words):
            return object_type

    raise ValueError(
        "Genesis does not recognize that object yet. "
        "Try a sword, tree, cube, or sphere."
    )


def route_prompt(prompt: str) -> trimesh.Scene:
    """Choose a generator and apply prompt attributes."""

    prompt_lower = prompt.lower().strip()

    scale = detect_scale(prompt_lower)
    material = detect_material(prompt_lower)
    object_type = detect_object_type(prompt_lower)

    if object_type == "sword":
        return create_sword(
            scale=scale,
            material=material,
        )

    if object_type == "tree":
        return create_tree(scale=scale)

    if object_type == "cube":
        cube = trimesh.creation.box(
            extents=(2 * scale, 2 * scale, 2 * scale),
        )
        return trimesh.Scene(cube)

    if object_type == "sphere":
        sphere = trimesh.creation.icosphere(
            subdivisions=3,
            radius=1.2 * scale,
        )
        return trimesh.Scene(sphere)

    raise ValueError("Unsupported object type.")