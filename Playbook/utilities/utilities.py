import bpy
import os
import math
import requests
import uuid
from dotenv import load_dotenv
from .. import __package__ as base_package


preferences = None


def get_env(key):
    # Determine the path to the .env file
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

    # Load the .env file
    load_dotenv(dotenv_path=env_path)

    return os.getenv(key)


def get_api_key() -> str:
    global preferences

    if not preferences:
        addon = bpy.context.preferences.addons.get(base_package)
        if addon:
            preferences = addon.preferences
        else:
            print(f"Could not get user preferences!")

    return preferences.api_key


#
def force_ui_redraw():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            area.tag_redraw()


#
def get_scaled_resolution_height(width: int):
    final_resolutions = get_final_resolutions()

    resolution_scale = width / final_resolutions["x"]
    return math.ceil(final_resolutions["y"] * resolution_scale)


#
def get_scale_resolution_width(height: int):
    final_resolutions = get_final_resolutions()

    resolution_scale = height / final_resolutions["y"]
    return math.ceil(final_resolutions["x"] * resolution_scale)


#
def get_final_resolutions():
    render = bpy.context.scene.render
    resolution_x = render.resolution_x
    resolution_y = render.resolution_y
    resolution_percentage = render.resolution_percentage

    final_resolution_x = resolution_x * (resolution_percentage / 100)
    final_resolution_y = resolution_y * (resolution_percentage / 100)

    return {"x": final_resolution_x, "y": final_resolution_y}


# Create a new simple RGB material
def create_rgb_material(name: str, color: tuple) -> bpy.types.Material:
    mat = bpy.data.materials.new(name=name)

    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear the material's nodes
    for node in nodes:
        nodes.remove(node)

    rgb_node = nodes.new(type="ShaderNodeRGB")
    rgb_node.outputs["Color"].default_value = color

    material_output = nodes.new(type="ShaderNodeOutputMaterial")

    # Link the created nodes
    mat.node_tree.links.new(
        rgb_node.outputs["Color"], material_output.inputs["Surface"]
    )

    return mat


# Convert a Blender FloatVectorProperty color to a hexadecimal color string
def color_to_hex(color) -> str:
    r, g, b, a = [int(c * 255) for c in color]

    # Format the RGBA components into a hex string
    hex_color = "#{:02X}{:02X}{:02X}{:02X}".format(r, g, b, a)

    return hex_color


# Function to download the image from a URL and save it locally
def download_image(url, save_path):
    try:
        print(f"URL: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Image downloaded successfully and saved to {save_path}")
    except Exception as e:
        print(f"Failed to download the image: {e}")


# Function to load the image into Blender
def load_image_into_blender(file_path):
    if os.path.exists(file_path):
        image = bpy.data.images.load(filepath=file_path)
        print(f"Image loaded into Blender: {image.name}")
        return image
    else:
        print(f"File does not exist: {file_path}")
        return None


#
def create_render_filename() -> str:
    uuid_str = str(uuid.uuid4())

    return f"Playbook_{uuid_str}.png"


#
def show_message_box(messages, title, icon="INFO"):

    def draw(self, context):
        for message in messages:
            self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

    return True
