from pathlib import Path

import numpy as np
import trimesh
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from generators.router import route_prompt


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
        scene = route_prompt(prompt)
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