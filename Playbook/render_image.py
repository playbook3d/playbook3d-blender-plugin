import asyncio
import bpy
import os
import threading
import base64
from .beauty_render import render_beauty_pass
from .mask_render import render_mask_pass
from .depth_render import render_depth_pass
from .outline_render import render_outline_pass
from .objects import visible_objects
from .properties import get_render_type
from .visible_objects import (
    set_visible_objects,
    save_object_materials,
    set_object_materials_opaque,
    reset_object_materials,
    color_hex,
)
from .comfy_deploy_api.network import (
    GlobalRenderSettings,
    RetextureRenderSettings,
    MaskData,
    StyleTransferRenderSettings,
    ComfyDeployClient,
)

# VARIABLES
api_url = os.getenv("API_URL")


# Returns True if an error occurs while attempting to render the image.
def error_exists_in_flow(scene) -> bool:
    # [workflow, condition for error message]
    workflow_checks = {
        # "EMAIL": scene.auth_properties.user_email == "Email",
        "APIKEY": bpy.context.preferences.addons.get("Playbook").preferences.api_key
        == "",
        "VISIBLEOBJECT": not visible_objects,
    }

    # [workflow, error message]
    messages = {
        "EMAIL": "Please login to render.",
        "APIKEY": "Copy your API key from the Playbook web editor.",
        "RETEXTURE": "Scene prompt is missing.",
        "STYLETRANSFER": "Style transfer image is missing.",
        "VISIBLEOBJECT": "No object(s) to render.",
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


#
def clear_render_folder():
    dir = os.path.dirname(__file__)
    folder_path = os.path.join(dir, "renders")

    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(path):
                    os.unlink(path)
            except Exception as e:
                print(f"Failed to delete {path}: {e}")


#
def clean_up_files():
    dir = os.path.dirname(__file__)
    folder_path = os.path.join(dir, "renders")

    if os.path.exists(folder_path):

        render_mist = os.path.join(folder_path, "render_mist.png")
        render_edge = os.path.join(folder_path, "render_edge.png")
        render_depth = os.path.join(folder_path, "depth0000.png")
        render_depth1 = os.path.join(folder_path, "depth0001.png")

        render_outline = os.path.join(folder_path, "outline0000.png")
        render_outline1 = os.path.join(folder_path, "outline0001.png")

        render_depth_new = os.path.join(folder_path, "depth.png")
        render_outline_new = os.path.join(folder_path, "outline.png")

        if os.path.exists(render_mist):
            os.remove(render_mist)
        if os.path.exists(render_edge):
            os.remove(render_edge)

        # Depth alternates between 0000 and 0001 and I don't know why
        if os.path.exists(render_depth):
            os.rename(render_depth, render_depth_new)
        elif os.path.exists(render_depth1):
            os.rename(render_depth1, render_depth_new)

        # Outline alternates between 0000 and 0001 and I don't know why
        if os.path.exists(render_outline):
            os.rename(render_outline, render_outline_new)
        elif os.path.exists(render_outline1):
            os.rename(render_outline1, render_outline_new)


# -------------------------------------------
# RENDER TO API
# -------------------------------------------


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

    render_type = get_render_type()

    mask_props = [
        MaskData(
            getattr(scene, f"{render_type}_mask_properties{index + 1}").mask_prompt,
            color_hex[f"MASK{index + 1}"],
        )
        for index in range(7)
    ]

    return RetextureRenderSettings(
        retexture_props.retexture_prompt,
        retexture_props.retexture_structure_strength,
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
    mask_path = os.path.join(dir, "renders", "mask.png")
    depth_path = os.path.join(dir, "renders", "depth.png")
    outline_path = os.path.join(dir, "renders", "outline.png")

    # Open the PNG files in binary mode
    with open(beauty_path, "rb") as beauty_file:
        beauty_blob = base64.b64encode(beauty_file.read())
    with open(mask_path, "rb") as mask_file:
        mask_blob = base64.b64encode(mask_file.read())
    with open(depth_path, "rb") as depth_file:
        depth_blob = base64.b64encode(depth_file.read())
    with open(outline_path, "rb") as outline_file:
        outline_blob = base64.b64encode(outline_file.read())

    comfy_deploy.save_image(beauty_blob, "beauty")
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

    print(f"Response: {response}")


#
def start_render_thread():
    render_thread = threading.Thread(target=render_image)
    render_thread.start()
    render_thread.join()


# Render the image from the active camera
def render_image():
    scene = bpy.context.scene

    # asyncio.run(PlaybookWebsocket().websocket_message())

    set_visible_objects(bpy.context)

    if error_exists_in_flow(scene):
        visible_objects.clear()
        return

    scene.is_rendering = True

    bpy.app.timers.register(continue_render, first_interval=0.1)


def continue_render():
    clear_render_folder()

    save_object_materials()

    # Set materials opaque for beauty and depth passes
    set_object_materials_opaque()

    # Render all required passes
    render_all_passes()

    reset_object_materials()

    clean_up_files()

    comfy = ComfyDeployClient()
    set_comfy_images(comfy)
    asyncio.run(run_comfy_workflow(comfy))

    return None


def render_all_passes():
    # Render unmodified image
    render_beauty_pass()
    # Render depth image
    render_depth_pass()
    # Render mask image
    render_mask_pass()
    # Render outline image
    render_outline_pass()
