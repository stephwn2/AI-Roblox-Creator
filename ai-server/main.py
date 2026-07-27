from pathlib import Path

import numpy as np
import trimesh
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from generators.router import route_prompt
from processing.asset_damage import (
    apply_broken_blade_damage,
)
from processing.asset_cleanup import (
    center_and_ground_scene,
    rotate_scene_x,
)
import traceback

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





@app.post("/generate")
def generate_model(request: GenerateRequest):
    prompt = request.prompt.strip()

    if not prompt:
        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty.",
        )

    try:
        # Generate the asset
        scene = route_prompt(prompt)

        # Apply damage if requested
        if "broken" in prompt.lower():
            scene = apply_broken_blade_damage(
                scene,
                damage_amount=0.45,
            )

        # Cleanup before exporting
        scene = center_and_ground_scene(scene)
        scene = rotate_scene_x(scene, -90)

    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    safe_name = "".join(
    character if character.isalnum() else "_"
    for character in prompt.lower()
    ).strip("_")

    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    model_path = (
        OUTPUT_DIRECTORY / f"{safe_name}.glb"
    ).resolve()

    scene.export(
        file_obj=str(model_path),
        file_type="glb",
    )

    print("EXPORTED MODEL:", model_path)
    print("FILE EXISTS:", model_path.exists())

    if not model_path.exists():
        raise RuntimeError(
            f"Model export failed: {model_path}"
        )

    return {
        "success": True,
        "filename": model_path.name,
        "path": str(model_path),
    }