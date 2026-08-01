from dataclasses import dataclass, field


@dataclass
class AssetModifiers:
    """Multipliers applied to procedural asset dimensions."""

    height: float = 1.0
    width: float = 1.0
    depth: float = 1.0

    trunk_height: float = 1.0
    trunk_radius: float = 1.0

    canopy_height: float = 1.0
    canopy_radius: float = 1.0

    blade_length: float = 1.0
    blade_width: float = 1.0

    guard_width: float = 1.0
    handle_length: float = 1.0

    extras: dict[str, float] = field(
        default_factory=dict,
    )


SIZE_MODIFIERS: dict[str, AssetModifiers] = {
    "tiny": AssetModifiers(
        height=0.45,
        width=0.55,
        depth=0.55,
        trunk_height=0.50,
        trunk_radius=0.65,
        canopy_height=0.55,
        canopy_radius=0.60,
        blade_length=0.60,
        blade_width=0.75,
        guard_width=0.75,
        handle_length=0.70,
    ),

    "small": AssetModifiers(
        height=0.75,
        width=0.80,
        depth=0.80,
        trunk_height=0.75,
        trunk_radius=0.82,
        canopy_height=0.78,
        canopy_radius=0.82,
        blade_length=0.80,
        blade_width=0.88,
        guard_width=0.88,
        handle_length=0.85,
    ),

    "normal": AssetModifiers(),

    "large": AssetModifiers(
        height=1.35,
        width=1.25,
        depth=1.25,
        trunk_height=1.35,
        trunk_radius=1.25,
        canopy_height=1.25,
        canopy_radius=1.30,
        blade_length=1.30,
        blade_width=1.15,
        guard_width=1.15,
        handle_length=1.20,
    ),

    "giant": AssetModifiers(
        height=1.80,
        width=1.55,
        depth=1.55,
        trunk_height=1.80,
        trunk_radius=1.55,
        canopy_height=1.55,
        canopy_radius=1.65,
        blade_length=1.65,
        blade_width=1.30,
        guard_width=1.30,
        handle_length=1.40,
    ),

    "massive": AssetModifiers(
        height=2.20,
        width=1.85,
        depth=1.85,
        trunk_height=2.20,
        trunk_radius=1.85,
        canopy_height=1.80,
        canopy_radius=1.95,
        blade_length=2.00,
        blade_width=1.45,
        guard_width=1.45,
        handle_length=1.65,
    ),
}


CONDITION_MODIFIERS: dict[str, AssetModifiers] = {
    "healthy": AssetModifiers(),

    "ancient": AssetModifiers(
        trunk_height=1.25,
        trunk_radius=1.65,
        canopy_radius=1.20,
        extras={
            "bend": 0.20,
        },
    ),

    "dead": AssetModifiers(
        canopy_height=0.35,
        canopy_radius=0.40,
        extras={
            "leaf_density": 0.15,
        },
    ),

    "lush": AssetModifiers(
        canopy_height=1.25,
        canopy_radius=1.35,
        extras={
            "leaf_density": 1.40,
        },
    ),

    "snowy": AssetModifiers(
        canopy_radius=1.10,
        extras={
            "snow_amount": 1.0,
        },
    ),
}


def multiply_modifiers(
    first: AssetModifiers,
    second: AssetModifiers,
) -> AssetModifiers:
    """Combine two modifier sets by multiplying matching values."""

    combined_extras = first.extras.copy()

    for key, value in second.extras.items():
        combined_extras[key] = (
            combined_extras.get(key, 1.0)
            * value
        )

    return AssetModifiers(
        height=first.height * second.height,
        width=first.width * second.width,
        depth=first.depth * second.depth,
        trunk_height=(
            first.trunk_height
            * second.trunk_height
        ),
        trunk_radius=(
            first.trunk_radius
            * second.trunk_radius
        ),
        canopy_height=(
            first.canopy_height
            * second.canopy_height
        ),
        canopy_radius=(
            first.canopy_radius
            * second.canopy_radius
        ),
        blade_length=(
            first.blade_length
            * second.blade_length
        ),
        blade_width=(
            first.blade_width
            * second.blade_width
        ),
        guard_width=(
            first.guard_width
            * second.guard_width
        ),
        handle_length=(
            first.handle_length
            * second.handle_length
        ),
        extras=combined_extras,
    )


def get_asset_modifiers(
    size: str = "normal",
    condition: str = "healthy",
) -> AssetModifiers:
    """Return combined size and condition modifiers."""

    normalized_size = size.strip().lower()
    normalized_condition = condition.strip().lower()

    size_modifiers = SIZE_MODIFIERS.get(
        normalized_size,
        SIZE_MODIFIERS["normal"],
    )

    condition_modifiers = CONDITION_MODIFIERS.get(
        normalized_condition,
        CONDITION_MODIFIERS["healthy"],
    )

    return multiply_modifiers(
        size_modifiers,
        condition_modifiers,
    )