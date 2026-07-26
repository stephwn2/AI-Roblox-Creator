import trimesh

from generators.nature_generator import create_tree
from generators.weapon_generator import create_sword


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


def route_prompt(prompt: str) -> trimesh.Scene:
    """Choose a generator and apply prompt attributes."""

    prompt_lower = prompt.lower().strip()
    scale = detect_scale(prompt_lower)

    weapon_words = (
        "sword",
        "blade",
    )

    nature_words = (
        "tree",
        "pine",
        "oak",
    )

    if any(word in prompt_lower for word in weapon_words):
        return create_sword(scale=scale)

    if any(word in prompt_lower for word in nature_words):
        return create_tree(scale=scale)

    if "cube" in prompt_lower or "box" in prompt_lower:
        cube = trimesh.creation.box(
            extents=(2 * scale, 2 * scale, 2 * scale),
        )
        return trimesh.Scene(cube)

    if "sphere" in prompt_lower or "ball" in prompt_lower:
        sphere = trimesh.creation.icosphere(
            subdivisions=3,
            radius=1.2 * scale,
        )
        return trimesh.Scene(sphere)

    raise ValueError(
        "Genesis does not recognize that object yet. "
        "Try sword, tree, cube, or sphere."
    )