from pathlib import Path

import numpy as np
import trimesh
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Genesis AI Server")

OUTPUT_DIRECTORY = Path(
    r"C:\Users\steph\AI-Roblox-Creator\outputs"
)
OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)


class GenerateRequest(BaseModel):
    prompt: str


@app.get("/")
def health_check():
    return {
        "status": "online",
        "service": "Genesis AI Server",
    }


def create_sword() -> trimesh.Scene:
    """Create a recognizable low-poly game sword."""

    # Long tapered blade made from custom vertices.
    blade_vertices = np.array([
        [-0.16, -0.05, 0.00],
        [ 0.16, -0.05, 0.00],
        [-0.16,  0.05, 0.00],
        [ 0.16,  0.05, 0.00],

        [-0.10, -0.04, 2.35],
        [ 0.10, -0.04, 2.35],
        [-0.10,  0.04, 2.35],
        [ 0.10,  0.04, 2.35],

        [ 0.00, -0.03, 2.75],
        [ 0.00,  0.03, 2.75],
    ])

    blade_faces = np.array([
        [0, 1, 3], [0, 3, 2],
        [0, 4, 5], [0, 5, 1],
        [2, 3, 7], [2, 7, 6],
        [0, 2, 6], [0, 6, 4],
        [1, 5, 7], [1, 7, 3],
        [4, 6, 9], [4, 9, 8],
        [5, 8, 9], [5, 9, 7],
        [4, 8, 5],
        [6, 7, 9],
    ])

    blade = trimesh.Trimesh(
        vertices=blade_vertices,
        faces=blade_faces,
        process=True,
    )
    blade.visual.face_colors = [175, 185, 195, 255]
    blade.apply_translation((0, 0, 0.55))

    # Crossguard.
    guard = trimesh.creation.box(
        extents=(1.25, 0.18, 0.18)
    )
    guard.visual.face_colors = [105, 72, 38, 255]
    guard.apply_translation((0, 0, 0.48))

    # Grip.
    handle = trimesh.creation.cylinder(
        radius=0.13,
        height=0.85,
        sections=12,
    )
    handle.visual.face_colors = [82, 48, 25, 255]
    handle.apply_translation((0, 0, 0.00))

    # End cap.
    pommel = trimesh.creation.icosphere(
        subdivisions=1,
        radius=0.20,
    )
    pommel.visual.face_colors = [105, 72, 38, 255]
    pommel.apply_translation((0, 0, -0.48))

    scene = trimesh.Scene()
    scene.add_geometry(blade, node_name="Blade")
    scene.add_geometry(guard, node_name="Guard")
    scene.add_geometry(handle, node_name="Handle")
    scene.add_geometry(pommel, node_name="Pommel")

    return scene


def create_tree() -> trimesh.Scene:
    trunk = trimesh.creation.cylinder(
        radius=0.35,
        height=2.5,
        sections=24,
    )
    trunk.apply_translation((0, 0, 1.25))

    leaves_bottom = trimesh.creation.cone(
        radius=1.3,
        height=2.2,
        sections=32,
    )
    leaves_bottom.apply_translation((0, 0, 2.6))

    leaves_top = trimesh.creation.cone(
        radius=0.9,
        height=1.8,
        sections=32,
    )
    leaves_top.apply_translation((0, 0, 3.8))

    scene = trimesh.Scene()
    scene.add_geometry(trunk, node_name="Trunk")
    scene.add_geometry(leaves_bottom, node_name="LeavesBottom")
    scene.add_geometry(leaves_top, node_name="LeavesTop")
    return scene


def generate_scene(prompt: str) -> trimesh.Scene:
    prompt_lower = prompt.lower()

    if "sword" in prompt_lower:
        return create_sword()

    if "tree" in prompt_lower:
        return create_tree()

    if "cube" in prompt_lower or "box" in prompt_lower:
        mesh = trimesh.creation.box(extents=(2, 2, 2))
        return trimesh.Scene(mesh)

    if "sphere" in prompt_lower or "ball" in prompt_lower:
        mesh = trimesh.creation.icosphere(
            subdivisions=3,
            radius=1.2,
        )
        return trimesh.Scene(mesh)

    raise ValueError(
        "Try a prompt containing cube, sphere, sword, or tree."
    )


@app.post("/generate")
def generate_model(request: GenerateRequest):
    prompt = request.prompt.strip()

    if not prompt:
        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty.",
        )

    try:
        scene = generate_scene(prompt)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    safe_name = "".join(
        character if character.isalnum() else "_"
        for character in prompt.lower()
    ).strip("_")

    model_path = OUTPUT_DIRECTORY / f"{safe_name}.glb"

    scene.export(
        file_obj=model_path,
        file_type="glb",
    )

    return {
        "status": "complete",
        "prompt": prompt,
        "message": f"Genesis generated: {prompt}",
        "model_path": str(model_path),
    }