

bl_info = {
    "name": "Genesis Engine",
    "author": "Stephen + ChatGPT",
    "version": (0, 2, 0),
    "blender": (5, 2, 0),
    "location": "View3D > Sidebar > Genesis",
    "description": "AI tools for Blender and Roblox",
    "category": "3D View",
}

import bpy
import os
import json
from urllib import request, error
from bpy.props import StringProperty


class GENESIS_OT_generate(bpy.types.Operator):
    bl_idname = "genesis.generate"
    bl_label = "Generate 3D"
    bl_description = "Generate a model using the entered prompt"

    def execute(self, context):
        prompt = context.scene.genesis_prompt.strip()

        if not prompt:
            self.report({"WARNING"}, "Enter a prompt first.")
            return {"CANCELLED"}

        payload = json.dumps({
            "prompt": prompt
        }).encode("utf-8")

        server_request = request.Request(
            "http://127.0.0.1:8000/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(server_request, timeout=60) as response:
                data = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            print(f"Genesis HTTP error {exc.code}: {error_body}")
            self.report({"ERROR"}, f"Server returned HTTP {exc.code}. Check console.")
            return {"CANCELLED"}

        except error.URLError as exc:
            print(f"Genesis connection error: {exc}")
            self.report({"ERROR"}, "Could not connect to Genesis server.")
            return {"CANCELLED"}
        except Exception as exc:
            self.report({"ERROR"}, f"Server error: {exc}")
            return {"CANCELLED"}

        model_path = data.get("path", "")

        if not os.path.isfile(model_path):
            self.report({"ERROR"}, "Generated model file was not found.")
            return {"CANCELLED"}

        objects_before = set(bpy.data.objects)

        bpy.ops.import_scene.gltf(filepath=model_path)

        imported_objects = [
            obj for obj in bpy.data.objects
            if obj not in objects_before
        ]

        if imported_objects:
            imported_objects[0].name = data["prompt"]

        self.report({"INFO"}, "Model imported successfully.")
        return {"FINISHED"}



class GENESIS_PT_panel(bpy.types.Panel):
    bl_label = "Genesis Engine"
    bl_idname = "GENESIS_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Genesis"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Describe your object:")
        layout.prop(context.scene, "genesis_prompt", text="")
        layout.operator("genesis.generate", icon="MESH_CUBE")


classes = (
    GENESIS_OT_generate,
    GENESIS_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.genesis_prompt = StringProperty(
        name="Prompt",
        description="Describe the 3D object to generate",
        default="",
        maxlen=250,
    )


def unregister():
    del bpy.types.Scene.genesis_prompt

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()