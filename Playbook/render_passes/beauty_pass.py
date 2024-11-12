import bpy
from ..utilities.utilities import get_parent_filepath

original_settings = {}


#
def save_beauty_settings():
    scene = bpy.context.scene

    original_settings.clear()
    original_settings.update({"use_nodes": scene.use_nodes})


#
def set_beauty_settings():
    scene = bpy.context.scene
    scene.use_nodes = False


#
def reset_beauty_settings():
    scene = bpy.context.scene
    scene.use_nodes = original_settings["use_nodes"]


#
def render_beauty_to_file():
    scene = bpy.context.scene
    render = scene.render

    output_path = get_parent_filepath("beauty.png", "renders")
    render.filepath = output_path

    if scene.camera:
        bpy.ops.render.render(write_still=True)

    else:
        print("No active camera found in the scene")


#
def render_beauty_pass():
    save_beauty_settings()
    set_beauty_settings()
    render_beauty_to_file()
    reset_beauty_settings()
