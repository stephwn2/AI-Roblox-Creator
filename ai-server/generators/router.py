import trimesh

from generators.nature_generator import create_tree
from generators.weapon_generator import create_sword


def route_prompt(prompt: str) -> trimesh.Scene:
    """Choose the correct generator based on words in the prompt."""

    prompt_lower = prompt.lower().strip()

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
        return create_sword()

    if any(word in prompt_lower for word in nature_words):
        return create_tree()

    if "cube" in prompt_lower or "box" in prompt_lower:
        cube = trimesh.creation.box(
            extents=(2, 2, 2),
        )
        return trimesh.Scene(cube)

    if "sphere" in prompt_lower or "ball" in prompt_lower:
        sphere = trimesh.creation.icosphere(
            subdivisions=3,
            radius=1.2,
        )
        return trimesh.Scene(sphere)

    raise ValueError(
        "Genesis does not recognize that object yet. "
        "Try sword, tree, cube, or sphere."
    )