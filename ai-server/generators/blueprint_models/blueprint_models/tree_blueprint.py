from dataclasses import dataclass


@dataclass
class TreeBlueprint:
    """Fully describes one procedural tree."""

    species: str = "pine"

    size: str = "normal"

    condition: str = "healthy"

    trunk_height: float = 2.5
    trunk_radius: float = 0.2

    lower_canopy_radius: float = 1.2
    lower_canopy_height: float = 2.0

    upper_canopy_radius: float = 0.8
    upper_canopy_height: float = 1.5

    trunk_sides: int = 10
    canopy_sections: int = 16

    bend: float = 0.0

    leaf_density: float = 1.0