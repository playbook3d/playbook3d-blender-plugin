import bpy
from ..utilities.file_utilities import get_filepath

original_settings = {}

def save_normal_settings():
    global original_settings
    scene = bpy.context.scene

    view = next((area.spaces[0] for area in bpy.context.screen.areas if area.type == 'VIEW_3D'), None)

    original_settings.clear()
    original_settings.update({
        "engine": scene.render.engine,
        "filepath": scene.render.filepath,
        "transparent": scene.render.film_transparent,
        "shading_type": view.shading.type if view else '',
        "studio_light": view.shading.studio_light if view else '',
    })

def set_normal_settings():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.film_transparent = False

    view = next((area.spaces[0] for area in bpy.context.screen.areas if area.type == 'VIEW_3D'), None)
    if view:
        view.shading.type = 'SOLID'
        view.shading.studio_light = 'studio.sl'  # RGB-based MatCap

def reset_normal_settings():
    scene = bpy.context.scene
    scene.render.engine = original_settings["engine"]
    scene.render.filepath = original_settings["filepath"]
    scene.render.film_transparent = original_settings["transparent"]

    view = next((area.spaces[0] for area in bpy.context.screen.areas if area.type == 'VIEW_3D'), None)
    if view:
        view.shading.type = original_settings["shading_type"]
        view.shading.studio_light = original_settings["studio_light"]

def render_normal_to_file():
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = get_filepath("renders/normal.png")
    bpy.ops.render.opengl(write_still=True)

def render_normal_pass():
    save_normal_settings()
    set_normal_settings()
    render_normal_to_file()
    reset_normal_settings()
