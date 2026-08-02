import trimesh

from generators.building_generator import create_building
from generators.fence_generator import create_fence
from generators.nature_generator import create_tree


def add_scene_with_translation(
    target_scene: trimesh.Scene,
    source_scene: trimesh.Scene,
    translation: tuple[float, float, float],
    name_prefix: str,
) -> None:
    """Copy every mesh from one scene into another with a translation."""

    for index, geometry in enumerate(
        source_scene.geometry.values(),
        start=1,
    ):
        copied_geometry = geometry.copy()
        copied_geometry.apply_translation(translation)

        target_scene.add_geometry(
            copied_geometry,
            node_name=f"{name_prefix}{index}",
        )


def create_walkway(
    width: float,
    length: float,
    thickness: float = 0.08,
) -> trimesh.Trimesh:
    """Create a simple path leading to the building entrance."""

    walkway = trimesh.creation.box(
        extents=(
            width,
            length,
            thickness,
        ),
    )

    walkway.visual.face_colors = [
        135,
        125,
        112,
        255,
    ]

    walkway.apply_translation(
        (
            0.0,
            0.0,
            thickness / 2,
        )
    )

    return walkway


def create_grass_lot(
    width: float,
    depth: float,
    thickness: float = 0.10,
) -> trimesh.Trimesh:
    """Create the ground slab for one property lot."""

    lot = trimesh.creation.box(
        extents=(
            width,
            depth,
            thickness,
        ),
    )

    lot.visual.face_colors = [
        72,
        125,
        65,
        255,
    ]

    lot.apply_translation(
        (
            0.0,
            0.0,
            -thickness / 2,
        )
    )

    return lot


def create_mailbox() -> trimesh.Scene:
    """Create a simple mailbox prop."""

    scene = trimesh.Scene()

    post = trimesh.creation.box(
        extents=(
            0.10,
            0.10,
            0.90,
        ),
    )

    post.visual.face_colors = [
        90,
        65,
        42,
        255,
    ]

    post.apply_translation(
        (
            0.0,
            0.0,
            0.45,
        )
    )

    scene.add_geometry(
        post,
        node_name="MailboxPost",
    )

    box = trimesh.creation.box(
        extents=(
            0.42,
            0.28,
            0.30,
        ),
    )

    box.visual.face_colors = [
        75,
        82,
        88,
        255,
    ]

    box.apply_translation(
        (
            0.0,
            0.0,
            0.95,
        )
    )

    scene.add_geometry(
        box,
        node_name="MailboxBox",
    )

    return scene


def create_house_lot(
    scale: float = 1.0,
    building_style: str = "house",
    building_material: str = "wood",
    condition: str = "clean",
    size: str = "normal",
    fence_material: str = "wood",
    tree_count: int = 2,
) -> trimesh.Scene:
    """Create a coordinated lot containing a building and yard assets."""

    scene = trimesh.Scene()

    lot_width = 12.0
    lot_depth = 14.0

    building_scene = create_building(
        scale=1.0,
        material=building_material,
        style=building_style,
        condition=condition,
        size=size,
        roof_style="automatic",
    )

    add_scene_with_translation(
        target_scene=scene,
        source_scene=building_scene,
        translation=(
            0.0,
            1.6,
            0.0,
        ),
        name_prefix="Building_",
    )

    grass = create_grass_lot(
        width=lot_width,
        depth=lot_depth,
    )

    scene.add_geometry(
        grass,
        node_name="GrassLot",
    )

    walkway = create_walkway(
        width=1.0,
        length=5.2,
    )

    walkway.apply_translation(
        (
            0.0,
            -3.1,
            0.02,
        )
    )

    scene.add_geometry(
        walkway,
        node_name="Walkway",
    )

    front_half_length = (
        lot_width - 2.2
    ) / 2

    front_left_fence = create_fence(
        length=front_half_length,
        material=fence_material,
    )

    add_scene_with_translation(
        target_scene=scene,
        source_scene=front_left_fence,
        translation=(
            -(front_half_length / 2 + 1.1),
            -lot_depth / 2,
            0.0,
        ),
        name_prefix="FrontLeftFence_",
    )

    front_right_fence = create_fence(
        length=front_half_length,
        material=fence_material,
    )

    add_scene_with_translation(
        target_scene=scene,
        source_scene=front_right_fence,
        translation=(
            front_half_length / 2 + 1.1,
            -lot_depth / 2,
            0.0,
        ),
        name_prefix="FrontRightFence_",
    )

    back_fence = create_fence(
        length=lot_width,
        material=fence_material,
    )

    add_scene_with_translation(
        target_scene=scene,
        source_scene=back_fence,
        translation=(
            0.0,
            lot_depth / 2,
            0.0,
        ),
        name_prefix="BackFence_",
    )

    left_fence = create_fence(
        length=lot_depth,
        material=fence_material,
    )

    for geometry in left_fence.geometry.values():
        geometry.apply_transform(
            trimesh.transformations.rotation_matrix(
                angle=1.57079632679,
                direction=(
                    0.0,
                    0.0,
                    1.0,
                ),
            )
        )

    add_scene_with_translation(
        target_scene=scene,
        source_scene=left_fence,
        translation=(
            -lot_width / 2,
            0.0,
            0.0,
        ),
        name_prefix="LeftFence_",
    )

    right_fence = create_fence(
        length=lot_depth,
        material=fence_material,
    )

    for geometry in right_fence.geometry.values():
        geometry.apply_transform(
            trimesh.transformations.rotation_matrix(
                angle=1.57079632679,
                direction=(
                    0.0,
                    0.0,
                    1.0,
                ),
            )
        )

    add_scene_with_translation(
        target_scene=scene,
        source_scene=right_fence,
        translation=(
            lot_width / 2,
            0.0,
            0.0,
        ),
        name_prefix="RightFence_",
    )

    mailbox_scene = create_mailbox()

    add_scene_with_translation(
        target_scene=scene,
        source_scene=mailbox_scene,
        translation=(
            -1.8,
            -lot_depth / 2 + 0.4,
            0.0,
        ),
        name_prefix="Mailbox_",
    )

    resolved_tree_count = max(
        int(tree_count),
        0,
    )

    tree_positions = [
        (
            -3.8,
            3.8,
            0.0,
        ),
        (
            3.8,
            3.5,
            0.0,
        ),
        (
            -4.0,
            -1.2,
            0.0,
        ),
        (
            4.0,
            -1.0,
            0.0,
        ),
    ]

    for tree_index in range(
        min(
            resolved_tree_count,
            len(tree_positions),
        )
    ):
        tree_scene = create_tree(
            scale=0.75,
            variation=True,
            tree_style="pine",
            condition="healthy",
            size="normal",
        )

        add_scene_with_translation(
            target_scene=scene,
            source_scene=tree_scene,
            translation=tree_positions[tree_index],
            name_prefix=f"Tree{tree_index + 1}_",
        )

    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)

    return scene