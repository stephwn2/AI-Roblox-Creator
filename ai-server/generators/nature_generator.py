import trimesh


def create_tree(scale: float = 1.0) -> trimesh.Scene:
    """Create a simple low-poly pine tree."""

    trunk = trimesh.creation.cylinder(
        radius=0.35,
        height=2.5,
        sections=12,
    )
    trunk.visual.face_colors = [92, 55, 28, 255]
    trunk.apply_translation((0, 0, 1.25))

    leaves_bottom = trimesh.creation.cone(
        radius=1.3,
        height=2.2,
        sections=16,
    )
    leaves_bottom.visual.face_colors = [42, 110, 52, 255]
    leaves_bottom.apply_translation((0, 0, 2.6))

    leaves_top = trimesh.creation.cone(
        radius=0.9,
        height=1.8,
        sections=16,
    )
    leaves_top.visual.face_colors = [52, 130, 62, 255]
    leaves_top.apply_translation((0, 0, 3.8))

    scene = trimesh.Scene()
    scene.add_geometry(trunk, node_name="Trunk")
    scene.add_geometry(leaves_bottom, node_name="LeavesBottom")
    scene.add_geometry(leaves_top, node_name="LeavesTop")

    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)
    return scene