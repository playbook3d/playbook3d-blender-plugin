import bpy
from .beauty_pass import render_beauty_pass
from .mask_pass import render_mask_pass
from .depth_pass import render_depth_pass
from .outline_pass import render_outline_pass
from .normal_pass import render_normal_pass
from ..objects.visible_objects import set_visible_objects
from ..objects.objects import visible_objects
from ..utilities.file_utilities import get_filepath
import os

original_render_engine = ""
original_settings = {}


# Returns a message if an error occurs while attempting to render the image.
def check_for_errors() -> bool:
    # [workflow, condition for error message]
    workflow_checks = {
        "VISIBLEOBJECT": not visible_objects,
    }

    # [workflow, error message]
    messages = {
        "VISIBLEOBJECT": "No object(s) to render.",
    }

    for key, val in workflow_checks.items():
        if val:
            return messages[key]

    return ""


# Is there an error when trying to render passes
def error_exists_in_render_passes():
    context = bpy.context

    set_visible_objects(context)

    error = check_for_errors()
    if not error:
        return False

    context.scene.error_message = error
    visible_objects.clear()
    return True


#
def render_passes(is_image: bool):
    set_render_layers()
    save_render_settings()
    set_render_settings()

    # Render all required passes
    render_selected_passes(is_image)

    # Safe cleanup of Render Result
    img = bpy.data.images.get("Render Result")
    if img and img.users == 0:
        bpy.data.images.remove(img)
        print("🧹 Cleaned up 'Render Result'")
    elif img:
        print(f"ℹ️ 'Render Result' in use, users={img.users}")
    else:
        print("ℹ️ No 'Render Result' image to remove")

    bpy.context.scene.node_tree.nodes.clear()
    reset_render_settings()


#
def set_render_layers():
    bpy.context.scene.use_nodes = True

    # Get the compositor node tree
    node_tree = bpy.context.scene.node_tree

    # Find the Render Layers node (or create one if it doesn't exist)
    render_layer_node = None
    for node in node_tree.nodes:
        if node.type == "R_LAYERS":
            render_layer_node = node
            break

    # If no Render Layers node is found, create one
    if render_layer_node is None:
        render_layer_node = node_tree.nodes.new(type="CompositorNodeRLayers")

    # Set the scene for the Render Layers node to the current scene
    render_layer_node.scene = bpy.context.scene


#
def save_render_settings():
    global original_render_engine

    scene = bpy.context.scene

    original_render_engine = ""
    original_settings.clear()

    if scene.render.engine != "EEVEE":
        original_render_engine = scene.render.engine
    else:
        original_settings.update(
            {
                "resolution": scene.render.resolution_percentage,
                "render_samples": scene.eevee.taa_render_samples,
            }
        )


#
def set_render_settings():
    scene = bpy.context.scene

    scene.render.resolution_percentage = 40
    scene.eevee.taa_render_samples = 16


#
def reset_render_settings():
    scene = bpy.context.scene

    if original_render_engine:
        scene.render.engine = original_render_engine
    elif original_settings:
        scene.render.resolution_percentage = original_settings["resolution"]
        scene.eevee.taa_render_samples = original_render_engine["render_samples"]

def render_selected_passes(is_image: bool):
    scene = bpy.context.scene
    render_props = scene.render_properties

    print("🖼️ Running selected passes...")

    # Always render beauty
    print("🎨 Rendering beauty pass...")
    render_beauty_pass(is_image)

    # Optional mask pass
    if render_props.mask_pass_checkbox:
        print("🎭 Rendering mask pass...")
        render_mask_pass(is_image)
    else:
        # ✅ If mask not selected, ensure mask.png is deleted
        mask_path = get_filepath("renders/mask.png")
        if os.path.exists(mask_path):
            os.remove(mask_path)
            print("🗑️ Removed unused mask pass output.")

    # Optional depth
    if render_props.depth_pass_checkbox and is_image:
        print("🌊 Rendering depth pass...")
        render_depth_pass()

    # Optional outline
    if render_props.outline_pass_checkbox and is_image:
        print("🖊️ Rendering outline pass...")
        render_outline_pass()

    print("✅ All selected passes rendered.")
