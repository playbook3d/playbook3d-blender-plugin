import bpy
import os
import time
from ..utilities.file_utilities import get_filepath

original_settings = {}

def save_beauty_settings():
    scene = bpy.context.scene
    shading = scene.display.shading
    space = next((area.spaces[0] for area in bpy.context.screen.areas if area.type == 'VIEW_3D'), None)

    original_settings.clear()
    original_settings.update({
        "engine": scene.render.engine,
        "filepath": scene.render.filepath,
        "use_nodes": scene.use_nodes,
        "image_format": scene.render.image_settings.file_format,
        "resolution_percentage": scene.render.resolution_percentage,
        "render_aa": scene.display.render_aa,
        "light": shading.light,
        "studio_light": shading.studio_light,
        "show_shadows": shading.show_shadows,
        "color_type": shading.color_type,
        "show_cavity": shading.show_cavity,
        "show_xray": shading.show_xray,
        "outline": shading.show_object_outline,
        "show_gizmo": space.show_gizmo if space else None,
        "overlay": space.overlay.show_overlays if space else None
    })

def set_beauty_settings(is_sequence=False):
    scene = bpy.context.scene
    shading = scene.display.shading
    space = next((area.spaces[0] for area in bpy.context.screen.areas if area.type == 'VIEW_3D'), None)

    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.render.image_settings.file_format = 'PNG'
    scene.render.resolution_percentage = 50
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
    shading.show_object_outline = True

    if space:
        space.show_gizmo = False
        space.overlay.show_overlays = False

def reset_beauty_settings():
    scene = bpy.context.scene
    shading = scene.display.shading
    space = next((area.spaces[0] for area in bpy.context.screen.areas if area.type == 'VIEW_3D'), None)

    scene.render.engine = original_settings["engine"]
    scene.render.filepath = original_settings["filepath"]
    scene.render.image_settings.file_format = original_settings["image_format"]
    scene.render.resolution_percentage = original_settings["resolution_percentage"]
    scene.use_nodes = original_settings["use_nodes"]
    scene.display.render_aa = original_settings["render_aa"]
    shading.light = original_settings["light"]
    shading.studio_light = original_settings["studio_light"]
    shading.show_shadows = original_settings["show_shadows"]
    shading.color_type = original_settings["color_type"]
    shading.show_cavity = original_settings["show_cavity"]
    shading.show_xray = original_settings["show_xray"]
    shading.show_object_outline = original_settings["outline"]

    if space:
        if original_settings["show_gizmo"] is not None:
            space.show_gizmo = original_settings["show_gizmo"]
        if original_settings["overlay"] is not None:
            space.overlay.show_overlays = original_settings["overlay"]

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

def wait_for_file(filepath, timeout=5.0):
    start = time.time()
    while not os.path.exists(filepath):
        if time.time() - start > timeout:
            print(f"❌ Timed out waiting for {filepath}")
            return False
        time.sleep(0.1)
    return True

def render_beauty(filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    bpy.context.scene.render.filepath = filepath

    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            with bpy.context.temp_override(area=area, region=area.regions[-1]):
                try:
                    bpy.ops.render.opengl(write_still=True, view_context=True)
                    print(f"🖼️ OpenGL render triggered to: {filepath}")
                except Exception as e:
                    print(f"❌ OpenGL render failed: {e}")
            break

    if wait_for_file(filepath):
        print(f"✅ File saved: {filepath}")
    else:
        print(f"❌ Render failed or file missing: {filepath}")

def render_beauty_as_image():
    filepath = get_filepath("renders/beauty.png")
    render_beauty(filepath)
    try_remove_render_result()

# Sequence timer state
capture_state = {
    "current_frame": 0,
    "end_frame": 0,
    "is_active": False,
    "timer_running": False
}

def render_beauty_sequence_timer():
    scene = bpy.context.scene
    if not capture_state["is_active"]:
        print("🛑 Sequence cancelled.")
        reset_beauty_settings()
        capture_state["timer_running"] = False
        return None

    frame = capture_state["current_frame"]
    if frame > capture_state["end_frame"]:
        print("✅ Sequence complete.")
        reset_beauty_settings()
        capture_state["is_active"] = False
        capture_state["timer_running"] = False
        return None

    scene.frame_set(frame)
    filepath = get_filepath(f"renders/beauty_zip/beauty_{frame:03}.png")
    render_beauty(filepath)
    try_remove_render_result()

    capture_state["current_frame"] += 1
    return 0.1 if capture_state["is_active"] else None

def start_beauty_sequence_capture():
    scene = bpy.context.scene
    save_beauty_settings()
    set_beauty_settings(is_sequence=True)

    capture_state["current_frame"] = scene.frame_start
    capture_state["end_frame"] = scene.frame_end
    capture_state["is_active"] = True

    print("🎬 Starting sequence capture...")
    if not capture_state["timer_running"]:
        capture_state["timer_running"] = True
        bpy.app.timers.register(render_beauty_sequence_timer)

def stop_beauty_sequence_capture():
    capture_state["is_active"] = False
    print("🛑 Sequence capture manually stopped.")

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
