import asyncio
import bpy
import os
import base64
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .render_passes.render_passes import render_passes, error_exists_in_render_passes
from .objects.object_utilities import mask_hex_colors
from .comfy_deploy_api.network import (
    GlobalRenderSettings,
    RetextureRenderSettings,
    MaskData,
    StyleTransferRenderSettings,
    ComfyDeployClient,
)
from .render_status import RenderStatus
from .utilities.utilities import get_api_key

# VARIABLES
api_url = os.getenv("API_URL")


# -------------------------------------------
# RENDER TO API
# -------------------------------------------


class RenderImage:

    @classmethod
    def render_image(cls):
        scene = bpy.context.scene
        scene.error_message = ""

        RenderStatus.is_rendering = True

        try:
            if error_exists_in_render_passes():
                RenderStatus.is_rendering = False
                return

            if error_exists_in_render_image(scene):
                RenderStatus.is_rendering = False
                return

            render_passes()

            comfy = ComfyDeployClient()
            set_comfy_images(comfy)
            workflow_message = asyncio.run(run_comfy_workflow(comfy))

            if workflow_message:
                scene.error_message = workflow_message
                RenderStatus.is_rendering = False

        except Exception as e:
            print(f"Error occurred: {e}")
            scene.error_message = "An error has occurred."
            RenderStatus.is_rendering = False


# Render the image according to the settings
class RenderImageOperator(Operator):
    bl_idname = "op.render_image"
    bl_label = "Run"
    bl_description = "Render the image"

    @classmethod
    def poll(cls, context):
        return not RenderStatus.is_rendering

    def execute(self, context):
        RenderImage.render_image()
        return {"FINISHED"}


#
def set_comfy_images(comfy_deploy: ComfyDeployClient):
    dir = os.path.dirname(__file__)

    beauty_path = os.path.join(dir, "renders", "beauty.png")
    normal_path = os.path.join(dir, "renders", "normal.png")
    mask_path = os.path.join(dir, "renders", "mask.png")
    depth_path = os.path.join(dir, "renders", "depth.png")
    outline_path = os.path.join(dir, "renders", "outline.png")

    # Open the PNG files in binary mode
    with open(beauty_path, "rb") as beauty_file:
        beauty_blob = base64.b64encode(beauty_file.read())
    with open(normal_path, "rb") as normal_file:
        normal_blob = base64.b64encode(normal_file.read())
    with open(mask_path, "rb") as mask_file:
        mask_blob = base64.b64encode(mask_file.read())
    with open(depth_path, "rb") as depth_file:
        depth_blob = base64.b64encode(depth_file.read())
    with open(outline_path, "rb") as outline_file:
        outline_blob = base64.b64encode(outline_file.read())

    comfy_deploy.save_image(beauty_blob, "beauty")
    comfy_deploy.save_image(normal_blob, "normal")
    comfy_deploy.save_image(mask_blob, "mask")
    comfy_deploy.save_image(depth_blob, "depth")
    comfy_deploy.save_image(outline_blob, "outline")


# Returns True if an error occurs while attempting to render the image.
def error_exists_in_render_image(scene) -> bool:
    # [workflow, condition for error message]
    workflow_checks = {
        "APIKEY": get_api_key() == "",
    }

    # [workflow, error message]
    messages = {
        "APIKEY": "Copy your API key from the Playbook web editor.",
    }

    for key, val in workflow_checks.items():
        if val:
            scene.error_message = messages[key]
            return True

    scene.error_message = ""
    return False


classes = [RenderImageOperator]


#
def register():
    global classes
    for cls in classes:
        register_class(cls)


#
def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)
