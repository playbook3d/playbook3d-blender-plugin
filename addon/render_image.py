import bpy
import requests
import io
import os
import base64
from .mask_render import save_mask_settings, set_mask_settings, reset_mask_settings
from .visible_objects import (
    save_object_materials,
    set_object_materials,
    reset_object_materials,
)
from .depth_render import set_depth_settings, render_depth_to_file
from .canny_render import (
    save_canny_settings,
    set_canny_settings,
    reset_canny_settings,
    render_canny_to_file,
)
from .properties import set_visible_objects

# VARIABLES

api_url = "https://api.playbookengine.com?token=MZLGGjo8JNn3O7EfyePoael1aPxAz1qFCrPGwKdpikDkd2QuJQ9GjYB68XuAz29B3ugJqx805X3N8Px3FDY6IASGYQeqimldsJa0TiRjF2o13124SwY2RCUzJkPA1XWI"


class RenderSettings:
    def __init__(
        self,
        style,
        prompt,
        structure_strength,
        # style_transfer_strength,
        # relight_strength,
        # relight_coordinates,
        # upres_value,
        # render_mode,
        # fixed_seed=False,
    ):
        self.style = style  # 0 = Photoreal, 1 = Anime, 2 = 3D Cartoon
        self.prompt = prompt
        self.structure_strength = structure_strength
        # self.style_transfer_strength = style_transfer_strength
        # self.relight_strength = relight_strength
        # self.relight_coordinates = relight_coordinates
        # self.upres_value = upres_value
        # self.render_mode = render_mode  # 0 = Render Image (Empty latent), 1 = Render Image (Re-render existing image)
        # self.fixed_seed = fixed_seed


class MaskData:
    def __init__(self, element_data, prompt, color):
        self.element_data = element_data
        self.prompt = prompt
        self.color = color


#
def clear_render_folder():
    dir = os.path.dirname(__file__)

    folder_path = os.path.join(dir, "renders")

    print(folder_path)
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(path):
                    os.unlink(path)
            except Exception as e:
                print(f"Failed to delete {path}: {e}")


# -------------------------------------------
# RENDER TO API
# -------------------------------------------


#
def render_to_buffer():
    # Create an off-screen buffer to render the image
    scene = bpy.context.scene
    render = scene.render

    # Ensure the render is done in RGBA mode
    render.image_settings.color_mode = "RGBA"
    render.image_settings.file_format = "PNG"

    # Render the image
    bpy.ops.render.render("INVOKE DEFAULT", write_still=True)

    # Get the rendered image
    rendered_image = bpy.data.images["Render Result"]

    # Save the image to a bytes buffer
    # buffer = io.BytesIO()
    # rendered_image.save_render(filepath="/dev/stdout", scene=scene)
    # rendered_image.pixels.foreach_get(buffer.write())

    # # Reset buffer position to the start
    # buffer.seek(0)

    # return buffer


#
def render_mask_to_file():
    scene = bpy.context.scene
    render = scene.render

    dir = os.path.dirname(__file__)

    output_path = os.path.join(dir, "renders", "render_color.png")
    render.filepath = output_path

    if scene.camera:
        bpy.ops.render.render(write_still=True)
        bpy.ops.render.view_show("INVOKE_DEFAULT")
    else:
        print("No active camera found in the scene")


#
def get_render_settings():
    scene = bpy.context.scene
    global_props = scene.global_properties

    render_settings = RenderSettings(
        style=global_props.global_style,
        prompt=global_props.global_prompt,
        structure_strength=global_props.global_structure_strength,
    )


#
def send_render_to_api(url):
    dir = os.path.dirname(__file__)

    render_path = os.path.join(dir, "renders", "render_color.png")

    print(f"Render path: {render_path}")

    # Open the PNG file in binary mode
    with open(render_path, "rb") as file:
        image_blob = base64.b64encode(file.read())

        # Send the POST request with the file
        response = requests.post(url, json={{"image": image_blob}})

        # Check the response status
        if response.status_code == 200:
            print("File uploaded successfully!")
        else:
            print(
                f"Failed to upload file. Status code: {response.status_code}, Response: {response.text}"
            )


# Render the image from the active camera
def render_image():
    print("----------------------------------------------")
    set_visible_objects(bpy.context)

    clear_render_folder()

    # Render mask image
    save_object_materials()
    save_mask_settings()
    set_object_materials()
    set_mask_settings()
    render_mask_to_file()
    reset_object_materials()
    reset_mask_settings()

    # Render depth image
    set_depth_settings()
    render_depth_to_file()

    # Render canny image
    set_canny_settings()
    render_canny_to_file()

    # TODO: Temp
    # get_render_settings()
    # Send the rendered image to API
    # buffer = render_to_buffer()
    # send_render_to_api(api_url, buffer)
