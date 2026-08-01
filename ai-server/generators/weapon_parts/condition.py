from copy import deepcopy


Color = list[int]
MaterialPalette = dict[str, Color]


def apply_condition_to_colors(
    colors: MaterialPalette,
    condition: str = "clean",
) -> MaterialPalette:
    """Apply a weapon condition to its color palette."""

    normalized_condition = condition.strip().lower()
    conditioned_colors = deepcopy(colors)

    if normalized_condition == "rusty":
        conditioned_colors["blade"] = [145, 74, 38, 255]
        conditioned_colors["guard"] = [115, 62, 35, 255]
        conditioned_colors["pommel"] = [105, 58, 34, 255]

    elif normalized_condition in {
        "old",
        "ancient",
        "aged",
    }:
        conditioned_colors["blade"] = darken_color(
            conditioned_colors["blade"],
            amount=30,
        )
        conditioned_colors["guard"] = darken_color(
            conditioned_colors["guard"],
            amount=25,
        )
        conditioned_colors["pommel"] = darken_color(
            conditioned_colors["pommel"],
            amount=20,
        )

    elif normalized_condition in {
        "enchanted",
        "magic",
        "magical",
    }:
        conditioned_colors["blade"] = brighten_color(
            conditioned_colors["blade"],
            amount=35,
        )
        conditioned_colors["guard"] = brighten_color(
            conditioned_colors["guard"],
            amount=20,
        )
        conditioned_colors["pommel"] = brighten_color(
            conditioned_colors["pommel"],
            amount=25,
        )

    elif normalized_condition in {
        "burned",
        "charred",
    }:
        conditioned_colors["blade"] = [55, 48, 45, 255]
        conditioned_colors["guard"] = [45, 40, 38, 255]
        conditioned_colors["handle"] = [35, 28, 25, 255]
        conditioned_colors["pommel"] = [42, 38, 36, 255]

    return conditioned_colors


def get_blade_condition_multiplier(
    condition: str = "clean",
) -> float:
    """Return the blade-length multiplier for a condition."""

    normalized_condition = condition.strip().lower()

    if normalized_condition in {
        "broken",
        "snapped",
    }:
        return 0.52

    if normalized_condition in {
        "chipped",
        "damaged",
    }:
        return 0.82

    return 1.0


def should_create_jagged_tip(
    condition: str = "clean",
) -> bool:
    """Return whether the blade should receive a damaged tip."""

    normalized_condition = condition.strip().lower()

    return normalized_condition in {
        "broken",
        "snapped",
        "chipped",
        "damaged",
    }


def darken_color(
    color: Color,
    amount: int,
) -> Color:
    """Darken an RGBA color without changing alpha."""

    red, green, blue, alpha = color

    return [
        max(red - amount, 0),
        max(green - amount, 0),
        max(blue - amount, 0),
        alpha,
    ]


def brighten_color(
    color: Color,
    amount: int,
) -> Color:
    """Brighten an RGBA color without changing alpha."""

    red, green, blue, alpha = color

    return [
        min(red + amount, 255),
        min(green + amount, 255),
        min(blue + amount, 255),
        alpha,
    ]