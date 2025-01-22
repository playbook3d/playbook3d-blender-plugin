import bpy
import os
import math
import requests
import uuid


def does_plugin_error_exists() -> bool:
    """
    Checks if there are any errors before attempting to render passes.
    Returns true if any errors are present.
    """

    # [error type, condition for error message]
    workflow_checks = {
        "APIKEY": bpy.context.preferences.addons.get(
            "bl_ext.user_default.Playbook"
        ).preferences.api_key
        == "",
    }

    # [error type, error message]
    error_messages = {
        "APIKEY": "Missing API key.",
    }

    for error_key, condition in workflow_checks.items():
        if condition:
            bpy.context.scene.error_message = error_messages[error_key]
            force_ui_redraw()
            return True

    bpy.context.scene.error_message = ""
    force_ui_redraw()
    return False


def force_ui_redraw():
    """
    Forces a manual redraw of Blender's UI.
    """

    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            area.tag_redraw()


def get_scaled_resolution_height(width: int):
    final_resolutions = get_final_resolutions()

    resolution_scale = width / final_resolutions["x"]
    return math.ceil(final_resolutions["y"] * resolution_scale)


def get_scale_resolution_width(height: int):
    final_resolutions = get_final_resolutions()

    resolution_scale = height / final_resolutions["y"]
    return math.ceil(final_resolutions["x"] * resolution_scale)


def get_final_resolutions():
    """
    Returns the current final resolution of the render camera in
    Blender.
    """

    render = bpy.context.scene.render
    resolution_x = render.resolution_x
    resolution_y = render.resolution_y
    resolution_percentage = render.resolution_percentage

    final_resolution_x = resolution_x * (resolution_percentage / 100)
    final_resolution_y = resolution_y * (resolution_percentage / 100)

    return {"x": final_resolution_x, "y": final_resolution_y}


def download_image(url, save_path):
    """
    Download an image from the given URL and save it locally.
    """

    try:
        print(f"URL: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Image downloaded successfully and saved to {save_path}")
    except Exception as e:
        print(f"Failed to download the image: {e}")


def load_image_into_blender(file_path):
    """
    Load the image from the given file path and load it into Blender.
    """

    if os.path.exists(file_path):
        image = bpy.data.images.load(filepath=file_path)
        print(f"Image loaded into Blender: {image.name}")
        return image
    else:
        print(f"File does not exist: {file_path}")
        return None


def create_render_filename() -> str:
    uuid_str = str(uuid.uuid4())

    return f"Playbook_{uuid_str}.png"


def show_message_box(messages, title, icon="INFO"):
    """
    Display a message box with the given message and title.
    """

    def draw(self, context):
        for message in messages:
            self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

    return True
