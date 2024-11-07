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


# Render the image according to the settings
class RenderImageOperator(Operator):
    bl_idname = "op.render_image"
    bl_label = "Render"
    bl_description = "Render the image"

    @classmethod
    def poll(cls, context):
        return not RenderStatus.is_rendering

    def execute(self, context):
        RenderImage.render_image()
        return {"FINISHED"}


#
def get_global_settings() -> GlobalRenderSettings:
    global_props = bpy.context.scene.global_properties

    return GlobalRenderSettings(
        global_props.global_workflow,
        global_props.global_model,
        global_props.global_style,
        0,
    )


#
def get_retexture_settings() -> RetextureRenderSettings:
    scene = bpy.context.scene

    retexture_props = scene.retexture_properties

    mask_props = [
        MaskData(
            getattr(scene, f"mask_properties{index + 1}").mask_prompt,
            mask_hex_colors[f"MASK{index + 1}"],
        )
        for index in range(7)
    ]

    return RetextureRenderSettings(
        retexture_props.retexture_prompt,
        retexture_props.retexture_structure_strength,
        retexture_props.preserve_texture_mask_index,
        *mask_props,
    )


#
def get_style_transfer_settings() -> StyleTransferRenderSettings:
    style_props = bpy.context.scene.style_properties

    return StyleTransferRenderSettings("", style_props.style_strength)


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

    style_path = bpy.context.scene.style_properties.style_image
    # Ensure the image is saved in a file or it's packed into the blend file
    if style_path:
        with open(style_path, "rb") as style_file:
            style_blob = base64.b64encode(style_file.read())

        comfy_deploy.save_image(style_blob, "style_transfer")


#
async def run_comfy_workflow(comfy_deploy: ComfyDeployClient):
    global_settings = get_global_settings()
    retexture_settings = get_retexture_settings()
    style_settings = get_style_transfer_settings()

    response = await comfy_deploy.run_workflow(
        global_settings, retexture_settings, style_settings
    )

    if response == "CREDITS":
        return "You don't have enough credits."
    elif response == "RENDER":
        return "Something went wrong."

    print(f"Response: {response}")


# Returns True if an error occurs while attempting to render the image.
def error_exists_in_render_image(scene) -> bool:
    # [workflow, condition for error message]
    workflow_checks = {
        "APIKEY": get_api_key() == "",
    }

    # [workflow, error message]
    messages = {
        "APIKEY": "Copy your API key from the Playbook web editor.",
        "RETEXTURE": "Scene prompt is missing.",
        "STYLETRANSFER": "Style transfer image is missing.",
    }

    if scene.global_properties.global_workflow == "RETEXTURE":
        workflow_checks["RETEXTURE"] = (
            scene.retexture_properties.retexture_prompt == "Describe the scene..."
        )
    elif scene.global_properties.global_workflow == "STYLETRANSFER":
        workflow_checks["STYLETRANSFER"] = not scene.style_properties.style_image

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
