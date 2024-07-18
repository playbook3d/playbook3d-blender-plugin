import bpy
import requests
import io
from .properties import visible_objects
from .color_management_settings import save_settings, set_settings, reset_settings
from .visible_objects import (
    save_object_materials,
    set_object_materials,
    reset_object_materials,
)

# VARIABLES

api_url = "https://api.playbookengine.com?token=MZLGGjo8JNn3O7EfyePoael1aPxAz1qFCrPGwKdpikDkd2QuJQ9GjYB68XuAz29B3ugJqx805X3N8Px3FDY6IASGYQeqimldsJa0TiRjF2o13124SwY2RCUzJkPA1XWI"

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
    bpy.ops.render.render(write_still=True)

    # Get the rendered image
    rendered_image = bpy.data.images["Render Result"]

    # Save the image to a bytes buffer
    buffer = io.BytesIO()
    rendered_image.save_render(filepath="/dev/stdout", scene=scene)
    rendered_image.pixels.foreach_get(buffer.write())

    # Reset buffer position to the start
    buffer.seek(0)

    return buffer


#
def send_render_to_api(url, file_path):
    # Open the PNG file in binary mode
    with open(file_path, "rb") as file:
        # Define the files dictionary
        files = {"file": ("render.png", file, "image/png")}

        # Send the POST request with the file
        response = requests.post(url, files=files)

        # Check the response status
        if response.status_code == 200:
            print("File uploaded successfully!")
        else:
            print(
                f"Failed to upload file. Status code: {response.status_code}, Response: {response.text}"
            )


# Render the image from the active camera
def render_image(context):
    # Save the scene to reset values later
    save_object_materials()
    save_settings()

    # Prepare the scene for render
    set_object_materials()
    set_settings()

    # Send the rendered image to API
    # buffer = render_to_buffer()
    # send_render_to_api(api_url, buffer)

    # Revert the scene to before the render
    reset_object_materials()
    reset_settings()
