import bpy
import os
import shutil
from .beauty_pass import render_beauty_pass
from .mask_pass import render_mask_pass
from .depth_pass import render_depth_pass
from .outline_pass import render_outline_pass
from .normal_pass import render_normal_pass
from ..objects.visible_objects import set_visible_objects
from ..objects.objects import visible_objects


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
def render_passes():
    # Render all required passes
    render_selected_passes()

    # Clean up renders
    bpy.data.images.remove(bpy.data.images["Render Result"])
    bpy.context.scene.node_tree.nodes.clear()


def render_selected_passes():
    bpy.context.scene.use_nodes = True

    render_properties = bpy.context.scene.render_properties

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

    if render_properties.beauty_pass_checkbox:
        # Render unmodified image
        render_beauty_pass()
    if render_properties.normal_pass_checkbox:
        # Render normal image
        render_normal_pass()
    if render_properties.mask_pass_checkbox:
        # Render mask image
        render_mask_pass()
    # Render depth image
    # render_depth_pass()
    if render_properties.outline_pass_checkbox:
        # Render outline image
        render_outline_pass()
