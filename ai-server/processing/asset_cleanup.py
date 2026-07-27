import trimesh


def center_and_ground_scene(scene: trimesh.Scene) -> trimesh.Scene:
    """Center a scene on X/Y and place its lowest point on Z = 0."""

    cleaned_scene = scene.copy()

    bounds = cleaned_scene.bounds
    minimum = bounds[0]
    maximum = bounds[1]

    center_x = (minimum[0] + maximum[0]) / 2.0
    center_y = (minimum[1] + maximum[1]) / 2.0
    minimum_z = minimum[2]

    translation = (
        -center_x,
        -center_y,
        -minimum_z,
    )

    for geometry in cleaned_scene.geometry.values():
        geometry.apply_translation(translation)

    return cleaned_scene


def rotate_scene_x(
    scene: trimesh.Scene,
    degrees: float,
) -> trimesh.Scene:
    """Rotate an entire scene around the X axis."""

    rotated_scene = scene.copy()

    rotation = trimesh.transformations.rotation_matrix(
        angle=degrees * 3.1415926535 / 180.0,
        direction=(1, 0, 0),
        point=(0, 0, 0),
    )

    for geometry in rotated_scene.geometry.values():
        geometry.apply_transform(rotation)

    return rotated_scene