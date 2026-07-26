from pathlib import Path

import numpy as np
import trimesh
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from generators.weapon_generator import create_sword
from generators.nature_generator import create_tree

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