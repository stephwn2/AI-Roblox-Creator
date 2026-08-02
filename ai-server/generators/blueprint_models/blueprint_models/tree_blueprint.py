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


@dataclass
class BuildingBlueprint:
    """Structured instructions for one procedural building."""

building_style: str = "house"
material: str = "wood"
condition: str = "clean"
size: str = "normal"

width: float = 3.0
depth: float = 3.0
wall_height: float = 2.5

floor_count: int = 1

roof_style: str = "gable"
roof_height: float = 1.2

door_count: int = 1
window_count: int = 4

has_chimney: bool = False
has_balcony: bool = False
has_tower: bool = False

wall_thickness: float = 0.18