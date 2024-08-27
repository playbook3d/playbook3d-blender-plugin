import bpy
import os


#
def render_beauty_pass():
    scene = bpy.context.scene
    render = scene.render

    dir = os.path.dirname(__file__)

    output_path = os.path.join(dir, "renders", "beauty.png")
    render.filepath = output_path

    if scene.camera:
        bpy.ops.render.render(write_still=True)

    else:
        print("No active camera found in the scene")
