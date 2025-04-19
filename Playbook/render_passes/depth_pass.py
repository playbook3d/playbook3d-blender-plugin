
import bpy
import os
from ..utilities.file_utilities import get_filepath

original_settings = {}

def save_depth_settings():
    scene = bpy.context.scene
    if not scene.world:
        scene.world = bpy.data.worlds.new(name="World")
    original_settings.clear()
    original_settings.update({
        "z_pass": bpy.context.view_layer.use_pass_z,
        "exposure": scene.view_settings.exposure,
        "gamma": scene.view_settings.gamma,
    })

def set_depth_settings():
    scene = bpy.context.scene
    view_layer = bpy.context.view_layer

    bpy.ops.preferences.addon_enable(module="cycles")
    scene.render.engine = "CYCLES"

    prefs = bpy.context.preferences.addons["cycles"].preferences
    scene.cycles.device = "GPU" if prefs.compute_device_type != "NONE" else "CPU"
    scene.cycles.samples = 1
    scene.cycles.use_adaptive_sampling = False
    scene.cycles.use_denoising = False
    scene.cycles.use_preview_denoising = False

    scene.render.film_transparent = False
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_depth = "16"

    view_layer.use_pass_z = True
    view_layer.use_pass_combined = False
    view_layer.use_pass_normal = False
    view_layer.use_pass_diffuse_color = False
    view_layer.use_pass_glossy_color = False
    view_layer.use_pass_emit = False
    view_layer.use_pass_ambient_occlusion = False
    view_layer.use_pass_shadow = False

    scene.view_settings.view_transform = "Standard"
    scene.view_settings.exposure = 1
    scene.view_settings.gamma = 1

def reset_depth_settings():
    scene = bpy.context.scene
    if "z_pass" in original_settings:
        bpy.context.view_layer.use_pass_z = original_settings["z_pass"]
        scene.view_settings.exposure = original_settings["exposure"]
        scene.view_settings.gamma = original_settings["gamma"]

def create_depth_compositing():
    scene = bpy.context.scene
    view_layer = bpy.context.view_layer

    if not scene.get("_z_pass_primed"):
        print("⚠️ Dummy render to register Depth output...")
        scene.render.use_compositing = False
        bpy.ops.render.render(write_still=False)
        scene.render.use_compositing = True
        scene["_z_pass_primed"] = True

    if not scene.camera:
        raise RuntimeError("❌ No active camera in the scene.")

    scene.use_nodes = True
    tree = scene.node_tree
    tree.nodes.clear()

    rl = tree.nodes.new("CompositorNodeRLayers")
    rl.scene = scene
    rl.layer = view_layer.name

    map_range = tree.nodes.new("CompositorNodeMapRange")
    invert = tree.nodes.new("CompositorNodeInvert")
    ramp = tree.nodes.new("CompositorNodeValToRGB")
    comp = tree.nodes.new("CompositorNodeComposite")
    viewer = tree.nodes.new("CompositorNodeViewer")

    ramp.color_ramp.interpolation = 'EASE'
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[1].position = 1.0

    map_range.inputs["From Min"].default_value = 0.1
    map_range.inputs["From Max"].default_value = 50.0

    if "Depth" not in rl.outputs:
        raise RuntimeError("❌ Depth pass is not available on Render Layers node.")

    tree.links.new(rl.outputs["Depth"], map_range.inputs["Value"])
    output_socket = map_range.outputs.get("Value") or map_range.outputs.get("Result")
    if not output_socket:
        raise RuntimeError("❌ MapRange node has no 'Value' or 'Result' output")
    tree.links.new(output_socket, ramp.inputs["Fac"])
    tree.links.new(ramp.outputs["Image"], invert.inputs["Color"])
    tree.links.new(invert.outputs["Color"], comp.inputs["Image"])
    tree.links.new(invert.outputs["Color"], viewer.inputs["Image"])

    print("✅ Depth compositor setup complete (dynamic Z-range, smooth falloff, scene-safe).")

def render_depth_to_file():
    scene = bpy.context.scene
    render = scene.render

    filepath = get_filepath("renders/depth.png")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    render.filepath = filepath
    create_depth_compositing()
    bpy.ops.render.render(write_still=True)
    print(f"✅ Depth pass saved to: {filepath}")

def render_depth_pass():
    save_depth_settings()
    set_depth_settings()
    try:
        render_depth_to_file()
    except Exception as e:
        print(f"❌ Error during depth render: {e}")
    finally:
        reset_depth_settings()
