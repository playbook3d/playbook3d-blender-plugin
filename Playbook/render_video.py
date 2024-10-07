import bpy
import os


def render_video():
    scene = bpy.context.scene
    camera = scene.camera

    if camera is None:
        return

    frame_rate = scene.render.fps

    start_frame = 0
    end_frame = int(3 * frame_rate)

    scene.frame_start = start_frame
    scene.frame_end = end_frame

    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            override = {"area": area}
            bpy.ops.view3d.view_camera(override)

    dir = os.path.dirname(__file__)
    output_path = os.path.join(dir, "renders", "video.png")

    scene.render.filepath = output_path

    scene.render.image_settings.file_format = "PNG"

    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            space = area.spaces.active
            space.shading.type = "RENDERED"

    bpy.ops.render.opengl(animation=True, view_context=True)
