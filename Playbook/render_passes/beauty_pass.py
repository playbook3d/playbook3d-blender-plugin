import bpy
from ..utilities.utilities import get_parent_filepath


#
def render_beauty_pass():
    scene = bpy.context.scene
    render = scene.render

    output_path = get_parent_filepath("beauty.png", "renders")
    render.filepath = output_path

    if scene.camera:
        bpy.ops.render.render(write_still=True)

    else:
        print("No active camera found in the scene")
