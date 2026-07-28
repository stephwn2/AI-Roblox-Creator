import trimesh

SHIELD_STYLES = {
    "round": {
        "radius": 1.0,
        "thickness": 0.18,
    },
    "tower": {
        "radius": 0.75,
        "thickness": 0.18,
    },
    "buckler": {
        "radius": 0.55,
        "thickness": 0.15,
    },
    "kite": {
        "radius": 0.75,
        "thickness": 0.16,
    },
}

def create_shield(
    scale: float = 1.0,
    material: str = "iron",
    style: str = "round",
) -> trimesh.Scene:
    """Create a simple low-poly shield."""

    style_settings = SHIELD_STYLES.get(
        style,
        SHIELD_STYLES["round"],
    )
    
    print(f"SHIELD STYLE = {style}")

    material_colors = {
        "wood": [125, 78, 38, 255],
        "iron": [175, 185, 195, 255],
        "gold": [212, 170, 45, 255],
    }

    color = material_colors.get(
        material,
        material_colors["iron"],
    )

    if style == "round":
        shield = trimesh.creation.cylinder(
            radius=style_settings["radius"],
            height=style_settings["thickness"],
            sections=24,
        )

    elif style == "buckler":
        shield = trimesh.creation.cylinder(
            radius=style_settings["radius"],
            height=style_settings["thickness"],
            sections=16,
        )

    elif style == "kite":
        width = style_settings["radius"] * 1.1
        height = style_settings["radius"] * 1.8
        thickness = style_settings["thickness"]

        vertices = [
            [-width / 2, -thickness / 2, height / 2],
            [ width / 2, -thickness / 2, height / 2],
            [ width / 2, -thickness / 2, 0.0],
            [ 0.0,       -thickness / 2, -height / 2],
            [-width / 2, -thickness / 2, 0.0],

            [-width / 2,  thickness / 2, height / 2],
            [ width / 2,  thickness / 2, height / 2],
            [ width / 2,  thickness / 2, 0.0],
            [ 0.0,        thickness / 2, -height / 2],
            [-width / 2,  thickness / 2, 0.0],
        ]

        faces = [
            [0, 1, 2], [0, 2, 4], [4, 2, 3],
            [5, 7, 6], [5, 9, 7], [9, 8, 7],

            [0, 5, 6], [0, 6, 1],
            [1, 6, 7], [1, 7, 2],
            [2, 7, 8], [2, 8, 3],
            [3, 8, 9], [3, 9, 4],
            [4, 9, 5], [4, 5, 0],
        ]

        shield = trimesh.Trimesh(
            vertices=vertices,
            faces=faces,
            process=True,
        )

    elif style == "tower":
        shield = trimesh.creation.box(
            extents=(
                style_settings["radius"] * 1.2,
                style_settings["thickness"],
                style_settings["radius"] * 2.2,
            ),
        )

    else:
        shield = trimesh.creation.cylinder(
            radius=style_settings["radius"],
            height=style_settings["thickness"],
            sections=24,
        )

    shield.visual.face_colors = color
    shield.apply_scale(scale)

    scene = trimesh.Scene()
    scene.add_geometry(
        shield,
        node_name="Shield",
    )

    return scene

