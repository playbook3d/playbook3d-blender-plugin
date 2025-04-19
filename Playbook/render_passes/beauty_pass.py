import bpy
import os
from ..utilities.file_utilities import get_filepath

original_settings = {}

def save_beauty_settings():
    scene = bpy.context.scene
    shading = scene.display.shading
    render = scene.render

    original_settings.clear()
    original_settings.update({
        "engine": render.engine,
        "filepath": render.filepath,
        "use_nodes": scene.use_nodes,
        "image_format": render.image_settings.file_format,
        "resolution_percentage": render.resolution_percentage,
        "render_aa": scene.display.render_aa,
        "light": shading.light,
        "studio_light": shading.studio_light,
        "show_shadows": shading.show_shadows,
        "color_type": shading.color_type,
        "show_cavity": shading.show_cavity,
        "show_xray": shading.show_xray,
        "outline": scene.display.shading.show_object_outline,
    })

def set_beauty_settings(is_sequence=False):
    scene = bpy.context.scene
    render = scene.render
    shading = scene.display.shading

    render.engine = 'BLENDER_WORKBENCH'
    render.image_settings.file_format = 'PNG'
    render.resolution_percentage = 50
    scene.use_nodes = False

    scene.display.render_aa = 'OFF'
    shading.light = 'STUDIO'
    shading.studio_light = 'Default'
    shading.show_shadows = False
    shading.color_type = 'SINGLE'
    shading.show_cavity = False
    shading.show_xray = False
    shading.use_scene_lights = False
    shading.use_scene_world = False

    # ✅ Enable outline
    scene.display.shading.show_object_outline = True

def reset_beauty_settings():
    scene = bpy.context.scene
    render = scene.render
    shading = scene.display.shading

    render.engine = original_settings["engine"]
    render.filepath = original_settings["filepath"]
    render.image_settings.file_format = original_settings["image_format"]
    render.resolution_percentage = original_settings["resolution_percentage"]
    scene.use_nodes = original_settings["use_nodes"]
    scene.display.render_aa = original_settings["render_aa"]
    shading.light = original_settings["light"]
    shading.studio_light = original_settings["studio_light"]
    shading.show_shadows = original_settings["show_shadows"]
    shading.color_type = original_settings["color_type"]
    shading.show_cavity = original_settings["show_cavity"]
    shading.show_xray = original_settings["show_xray"]
    scene.display.shading.show_object_outline = original_settings["outline"]

def try_remove_render_result():
    try:
        img = bpy.data.images.get("Render Result")
        if img and img.users == 0:
            bpy.data.images.remove(img)
            print("🧹 Removed 'Render Result'")
        elif img:
            print(f"ℹ️ 'Render Result' not removed (in use, users={img.users})")
    except Exception as e:
        print(f"⚠️ Error removing Render Result: {e}")

def render_beauty(filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    bpy.context.scene.render.filepath = filepath
    try:
        bpy.ops.render.render(write_still=True)
        print(f"✅ Rendered beauty to: {filepath}")
    except Exception as e:
        print(f"❌ Render failed: {e}")

def render_beauty_as_image():
    filepath = get_filepath("renders/beauty.png")
    render_beauty(filepath)
    try_remove_render_result()

# Timer state
capture_state = {
    "current_frame": 0,
    "end_frame": 0,
    "is_active": False,
    "timer_running": False
}

def render_beauty_sequence_timer():
    scene = bpy.context.scene
    if not capture_state["is_active"]:
        print("🛑 Render sequence was aborted.")
        reset_beauty_settings()
        capture_state["timer_running"] = False
        return None

    frame = capture_state["current_frame"]
    if frame > capture_state["end_frame"]:
        print("✅ Completed all frames.")
        reset_beauty_settings()
        capture_state["is_active"] = False
        capture_state["timer_running"] = False
        return None

    scene.frame_set(frame)
    filepath = get_filepath(f"renders/beauty_zip/beauty_{frame:03}.png")
    render_beauty(filepath)
    try_remove_render_result()

    # Queue next frame if still active
    capture_state["current_frame"] += 1
    if capture_state["is_active"]:
        return 0.1
    else:
        print("🛑 Sequence interrupted after frame render.")
        reset_beauty_settings()
        capture_state["timer_running"] = False
        return None

def start_beauty_sequence_capture():
    scene = bpy.context.scene
    save_beauty_settings()
    set_beauty_settings(is_sequence=True)

    capture_state["current_frame"] = scene.frame_start
    capture_state["end_frame"] = scene.frame_end
    capture_state["is_active"] = True

    print("🎬 Starting beauty pass sequence...")
    if not capture_state["timer_running"]:
        capture_state["timer_running"] = True
        bpy.app.timers.register(render_beauty_sequence_timer)

def stop_beauty_sequence_capture():
    capture_state["is_active"] = False
    print("🔴 User requested stop.")

def render_beauty_pass(is_image: bool):
    if is_image:
        save_beauty_settings()
        set_beauty_settings()
        try:
            render_beauty_as_image()
        finally:
            reset_beauty_settings()
    else:
        start_beauty_sequence_capture()