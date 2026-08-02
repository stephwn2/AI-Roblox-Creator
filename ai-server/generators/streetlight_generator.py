import trimesh


def create_streetlight(
    scale: float = 1.0,
) -> trimesh.Scene:

    scene = trimesh.Scene()

    pole_color = [110, 110, 110, 255]
    lamp_color = [230, 230, 180, 255]

    # Pole
    pole = trimesh.creation.cylinder(
        radius=0.05,
        height=2.8,
        sections=12,
    )

    pole.apply_translation((0, 0, 1.4))
    pole.visual.face_colors = pole_color
    scene.add_geometry(pole)

    # Arm
    arm = trimesh.creation.box(
        extents=(0.55, 0.05, 0.05),
    )

    arm.apply_translation((0.27, 0, 2.75))
    arm.visual.face_colors = pole_color
    scene.add_geometry(arm)

    # Lamp
    lamp = trimesh.creation.box(
        extents=(0.18, 0.12, 0.10),
    )

    lamp.apply_translation((0.55, 0, 2.68))
    lamp.visual.face_colors = lamp_color
    scene.add_geometry(lamp)

    # Base
    base = trimesh.creation.cylinder(
        radius=0.10,
        height=0.08,
        sections=16,
    )

    base.apply_translation((0, 0, 0.04))
    base.visual.face_colors = pole_color
    scene.add_geometry(base)

    for geometry in scene.geometry.values():
        geometry.apply_scale(scale)

    return scene