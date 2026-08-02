import trimesh


def create_wall(
    width: float,
    depth: float,
    height: float,
    color: list[int],
    position: tuple[float, float, float],
) -> trimesh.Trimesh:
    """Create one wall section."""

    wall = trimesh.creation.box(
        extents=(
            max(width, 0.05),
            max(depth, 0.05),
            max(height, 0.05),
        ),
    )

    wall.visual.face_colors = color
    wall.apply_translation(position)

    return wall


def create_exterior_walls(
    width: float,
    depth: float,
    height: float,
    thickness: float,
    doorway_width: float,
    doorway_height: float,
    color: list[int],
) -> list[tuple[str, trimesh.Trimesh]]:
    """Create hollow exterior walls with a real front doorway."""

    walls: list[tuple[str, trimesh.Trimesh]] = []

    half_width = width / 2
    half_depth = depth / 2
    half_height = height / 2

    left_wall = create_wall(
        width=thickness,
        depth=depth,
        height=height,
        color=color,
        position=(
            -(half_width - thickness / 2),
            0.0,
            half_height,
        ),
    )

    walls.append(
        (
            "LeftWall",
            left_wall,
        )
    )

    right_wall = create_wall(
        width=thickness,
        depth=depth,
        height=height,
        color=color,
        position=(
            half_width - thickness / 2,
            0.0,
            half_height,
        ),
    )

    walls.append(
        (
            "RightWall",
            right_wall,
        )
    )

    back_wall = create_wall(
        width=width - thickness * 2,
        depth=thickness,
        height=height,
        color=color,
        position=(
            0.0,
            half_depth - thickness / 2,
            half_height,
        ),
    )

    walls.append(
        (
            "BackWall",
            back_wall,
        )
    )

    front_side_width = max(
        (
            width
            - doorway_width
            - thickness * 2
        ) / 2,
        0.05,
    )

    front_left = create_wall(
        width=front_side_width,
        depth=thickness,
        height=height,
        color=color,
        position=(
            -(
                doorway_width / 2
                + front_side_width / 2
            ),
            -(half_depth - thickness / 2),
            half_height,
        ),
    )

    walls.append(
        (
            "FrontWallLeft",
            front_left,
        )
    )

    front_right = create_wall(
        width=front_side_width,
        depth=thickness,
        height=height,
        color=color,
        position=(
            doorway_width / 2
            + front_side_width / 2,
            -(half_depth - thickness / 2),
            half_height,
        ),
    )

    walls.append(
        (
            "FrontWallRight",
            front_right,
        )
    )

    doorway_header_height = max(
        height - doorway_height,
        0.0,
    )

    if doorway_header_height > 0.05:
        doorway_header = create_wall(
            width=doorway_width,
            depth=thickness,
            height=doorway_header_height,
            color=color,
            position=(
                0.0,
                -(half_depth - thickness / 2),
                doorway_height
                + doorway_header_height / 2,
            ),
        )

        walls.append(
            (
                "DoorwayHeader",
                doorway_header,
            )
        )

    return walls


def create_interior_wall_with_doorway(
    width: float,
    height: float,
    thickness: float,
    doorway_width: float,
    doorway_height: float,
    color: list[int],
    y_position: float = 0.0,
) -> list[tuple[str, trimesh.Trimesh]]:
    """Create one interior divider with a centered doorway."""

    walls: list[tuple[str, trimesh.Trimesh]] = []

    side_width = max(
        (width - doorway_width) / 2,
        0.05,
    )

    left_section = create_wall(
        width=side_width,
        depth=thickness,
        height=height,
        color=color,
        position=(
            -(doorway_width / 2 + side_width / 2),
            y_position,
            height / 2,
        ),
    )

    walls.append(
        (
            "InteriorWallLeft",
            left_section,
        )
    )

    right_section = create_wall(
        width=side_width,
        depth=thickness,
        height=height,
        color=color,
        position=(
            doorway_width / 2 + side_width / 2,
            y_position,
            height / 2,
        ),
    )

    walls.append(
        (
            "InteriorWallRight",
            right_section,
        )
    )

    header_height = max(
        height - doorway_height,
        0.0,
    )

    if header_height > 0.05:
        header = create_wall(
            width=doorway_width,
            depth=thickness,
            height=header_height,
            color=color,
            position=(
                0.0,
                y_position,
                doorway_height + header_height / 2,
            ),
        )

        walls.append(
            (
                "InteriorDoorwayHeader",
                header,
            )
        )

    return walls