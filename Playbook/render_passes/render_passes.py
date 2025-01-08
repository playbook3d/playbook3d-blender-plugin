import bpy
from .beauty_pass import render_beauty_pass
from .mask_pass import render_mask_pass
from .depth_pass import render_depth_pass
from .outline_pass import render_outline_pass
from .normal_pass import render_normal_pass
from ..objects.visible_objects import set_visible_objects
from ..objects.objects import visible_objects

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

    # Clean up renders
    bpy.data.images.remove(bpy.data.images["Render Result"])
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

    scene.render.resolution_percentage = 50
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
    render_properties = bpy.context.scene.render_properties

    if render_properties.beauty_pass_checkbox:
        # Render unmodified image
        render_beauty_pass(is_image)
    if render_properties.normal_pass_checkbox and is_image:
        # Render normal image
        render_normal_pass()
    if render_properties.mask_pass_checkbox:
        # Render mask image
        render_mask_pass(is_image)
    # Render depth image
    # render_depth_pass()
    if render_properties.outline_pass_checkbox and is_image:
        # Render outline image
        render_outline_pass()
