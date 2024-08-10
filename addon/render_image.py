import bpy
import requests
import io
import os
import base64
from .beauty_render import render_beauty_pass
from .mask_render import render_mask_pass
from .depth_render import render_depth_pass
from .outline_render import render_outline_pass
from .workspace import open_render_window
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
        render_outline = os.path.join(folder_path, "outline0001.png")
        render_depth_new = os.path.join(folder_path, "depth.png")
        render_outline_new = os.path.join(folder_path, "outline.png")

        if os.path.exists(render_mist):
            os.remove(render_mist)
        if os.path.exists(render_edge):
            os.remove(render_edge)

        if os.path.exists(render_depth):
            os.rename(render_depth, render_depth_new)
        if os.path.exists(render_outline):
            os.rename(render_outline, render_outline_new)


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

    # Render unmodified image
    render_beauty_pass()

    # Render mask image
    render_mask_pass()

    # Render depth image
    render_depth_pass()

    # Render outline image
    render_outline_pass()

    # Open the render workspace
    open_render_window()

    clean_up_files()
