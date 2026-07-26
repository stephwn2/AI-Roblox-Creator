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
    blade = trimesh.creation.box(
        extents=(0.18, 0.08, 2.8)
    )
    blade.apply_translation((0, 0, 1.7))

    guard = trimesh.creation.box(
        extents=(1.1, 0.18, 0.18)
    )
    guard.apply_translation((0, 0, 0.3))

    handle = trimesh.creation.cylinder(
        radius=0.13,
        height=0.9,
        sections=24,
    )
    handle.apply_translation((0, 0, -0.25))

    pommel = trimesh.creation.icosphere(
        subdivisions=2,
        radius=0.2,
    )
    pommel.apply_translation((0, 0, -0.75))

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