import asyncio
import bpy
import os
import base64
from .beauty_render import render_beauty_to_file
from .mask_render import (
    save_mask_settings,
    set_mask_settings,
    reset_mask_settings,
    render_mask_to_file,
)
from .visible_objects import (
    save_object_materials,
    set_object_materials,
    reset_object_materials,
    color_hex,
)
from .depth_render import (
    save_depth_settings,
    set_depth_settings,
    reset_depth_settings,
    render_depth_to_file,
)
from .canny_render import (
    save_canny_settings,
    set_canny_settings,
    reset_canny_settings,
    render_canny_to_file,
)
from .properties import set_visible_objects
from .utilities import color_to_hex
from .comfy_deploy_api.network import (
    GeneralSettings,
    MaskSettings,
    StyleTransferSettings,
    RelightSettings,
    UpscaleSettings,
    ComfyDeployClient,
)

# VARIABLES

api_url = "https://api.playbookengine.com?token=MZLGGjo8JNn3O7EfyePoael1aPxAz1qFCrPGwKdpikDkd2QuJQ9GjYB68XuAz29B3ugJqx805X3N8Px3FDY6IASGYQeqimldsJa0TiRjF2o13124SwY2RCUzJkPA1XWI"


class MaskData:
    def __init__(self, element_data, prompt, color):
        self.element_data = element_data
        self.prompt = prompt
        self.color = color


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
        render_depth = os.path.join(folder_path, "depth0001.png")
        render_canny = os.path.join(folder_path, "outline0001.png")
        render_depth_new = os.path.join(folder_path, "depth.png")
        render_canny_new = os.path.join(folder_path, "outline.png")

        if os.path.exists(render_mist):
            os.remove(render_mist)
        if os.path.exists(render_edge):
            os.remove(render_edge)

        if os.path.exists(render_depth):
            os.rename(render_depth, render_depth_new)
        if os.path.exists(render_canny):
            os.rename(render_canny, render_canny_new)


# -------------------------------------------
# RENDER TO API
# -------------------------------------------


#
def get_general_settings() -> GeneralSettings:
    general_props = bpy.context.scene.general_properties

    return GeneralSettings(
        general_props.general_style,
        general_props.general_prompt,
        general_props.general_structure_strength,
    )


#
def get_mask_settings(index: int) -> MaskSettings:
    mask_props = getattr(bpy.context.scene, f"mask_properties{index}")

    return MaskSettings(mask_props.mask_prompt, color_hex[f"MASK{index}"])


#
def get_style_transfer_settings() -> StyleTransferSettings:
    style_props = bpy.context.scene.style_properties

    return StyleTransferSettings(style_props.style_strength)


#
def get_relight_settings() -> RelightSettings:
    relight_props = bpy.context.scene.relight_properties

    return RelightSettings(
        color_to_hex(relight_props.relight_color),
        relight_props.relight_prompt,
        relight_props.relight_angle,
    )


#
def get_upscale_settings() -> UpscaleSettings:
    upscale_props = bpy.context.scene.upscale_properties

    return UpscaleSettings(upscale_props.upscale_scale)


#
def set_comfy_images(comfy_deploy: ComfyDeployClient):
    dir = os.path.dirname(__file__)

    beauty_path = os.path.join(dir, "renders", "beauty.png")
    mask_path = os.path.join(dir, "renders", "mask.png")
    depth_path = os.path.join(dir, "renders", "depth.png")
    outline_path = os.path.join(dir, "renders", "outline.png")

    print(f"Render path: {beauty_path}")
    print(f"Render path: {mask_path}")
    print(f"Render path: {depth_path}")
    print(f"Render path: {outline_path}")

    # Open the PNG file in binary mode
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


#
async def run_comfy_workflow(comfy_deploy: ComfyDeployClient):
    flags = bpy.context.scene.flag_properties

    general_settings = get_general_settings()
    mask_settings1 = get_mask_settings(1)
    mask_settings2 = get_mask_settings(2)
    mask_settings3 = get_mask_settings(3)
    mask_settings4 = get_mask_settings(4)
    mask_settings5 = get_mask_settings(5)
    mask_settings6 = get_mask_settings(6)
    mask_settings7 = get_mask_settings(7)
    style_settings = get_style_transfer_settings()
    relight_settings = get_relight_settings()
    upscale_settings = get_upscale_settings()

    response = await comfy_deploy.run_workflow(
        general_settings,
        mask_settings1,
        mask_settings2,
        mask_settings3,
        mask_settings4,
        mask_settings5,
        mask_settings6,
        mask_settings7,
        False,
        style_settings,
        relight_settings,
        upscale_settings,
        0,
        flags.retexture_flag,
        flags.style_flag,
        flags.relight_flag,
        flags.upscale_flag,
    )

    print(response)


# Render the image from the active camera
def render_image():
    print("----------------------------------------------")

    set_visible_objects(bpy.context)
    clear_render_folder()

    # Render unmodified image
    render_beauty_to_file()

    # Render mask image
    save_object_materials()
    save_mask_settings()
    set_object_materials()
    set_mask_settings()
    render_mask_to_file()
    reset_object_materials()
    reset_mask_settings()

    # Render depth image
    save_depth_settings()
    set_depth_settings()
    render_depth_to_file()
    reset_depth_settings()

    # Render canny image
    save_canny_settings()
    set_canny_settings()
    render_canny_to_file()
    reset_canny_settings()

    clean_up_files()

    comfy = ComfyDeployClient()
    set_comfy_images(comfy)
    asyncio.run(run_comfy_workflow(comfy))
