import bpy
from ..utilities.file_utilities import get_filepath

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
def render_beauty_as_image():
    filepath = get_filepath("renders/beauty.png")

    render_to_path(filepath)


#
def render_beauty_as_sequence():
    capture_count = bpy.context.scene.render_properties.capture_count

    filepath = get_filepath(f"renders/beauty_zip/beauty_{capture_count:03}.png")

    render_to_path(filepath)


#
def render_to_path(filepath: str):
    scene = bpy.context.scene
    render = scene.render

    render.filepath = filepath

    if scene.camera:
        bpy.ops.render.render(write_still=True)

    else:
        print("No active camera found in the scene")


#
def render_beauty_pass(is_image: bool):
    save_beauty_settings()
    set_beauty_settings()

    if is_image:
        render_beauty_as_image()
    else:
        render_beauty_as_sequence()

    reset_beauty_settings()
