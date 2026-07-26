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
    """Read a size word and return a scale multiplier."""

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
    """Detect a basic material word."""

    prompt_lower = prompt.lower()

    if any(word in prompt_lower for word in ("gold", "golden")):
        return "gold"

    if any(word in prompt_lower for word in ("wood", "wooden")):
        return "wood"

    if any(word in prompt_lower for word in ("iron", "steel", "metal")):
        return "iron"

    return "iron"


def detect_object_types(prompt: str) -> list[str]:
    """Find every supported object mentioned in the prompt."""

    prompt_lower = prompt.lower()
    detected_objects: list[str] = []

    for object_type, words in OBJECT_SYNONYMS.items():
        if any(word in prompt_lower for word in words):
            detected_objects.append(object_type)

    if not detected_objects:
        raise ValueError(
            "Genesis does not recognize any supported objects. "
            "Try sword, tree, cube, or sphere."
        )

    return detected_objects


def create_object_scene(
    object_type: str,
    scale: float,
    material: str,
) -> trimesh.Scene:
    """Generate one object scene."""

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

    raise ValueError(f"Unsupported object type: {object_type}")


def route_prompt(prompt: str) -> trimesh.Scene:
    """Generate every supported object mentioned in the prompt."""

    prompt_lower = prompt.lower().strip()

    scale = detect_scale(prompt_lower)
    material = detect_material(prompt_lower)
    object_types = detect_object_types(prompt_lower)

    combined_scene = trimesh.Scene()
    spacing = 5.0

    for object_index, object_type in enumerate(object_types):
        object_scene = create_object_scene(
            object_type=object_type,
            scale=scale,
            material=material,
        )

        centered_index = object_index - ((len(object_types) - 1) / 2)
        x_offset = centered_index * spacing

        for geometry_index, geometry in enumerate(
            object_scene.geometry.values()
        ):
            geometry_copy = geometry.copy()
            geometry_copy.apply_translation(
                (x_offset, 0.0, 0.0)
            )

            unique_name = (
                f"{object_type}_"
                f"{object_index}_"
                f"{geometry_index}"
            )

            combined_scene.add_geometry(
                geometry_copy,
                node_name=unique_name,
                geom_name=unique_name,
            )

    return combined_scene