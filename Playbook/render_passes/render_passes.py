import bpy
import os
import shutil
from .beauty_pass import render_beauty_pass
from .mask_pass import render_mask_pass
from .depth_pass import render_depth_pass
from .outline_pass import render_outline_pass
from ..visible_objects import (
    set_visible_objects,
    save_object_materials,
    set_object_materials_opaque,
    reset_object_materials,
)
from ..objects import visible_objects


# Returns True if an error occurs while attempting to render the image.
def error_exists_in_render_passes(scene) -> bool:
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
            scene.error_message = messages[key]
            return True

    scene.error_message = ""
    return False


def render_passes():
    context = bpy.context

    set_visible_objects(context)

    if error_exists_in_render_passes(context.scene):
        visible_objects.clear()
        return False

    continue_render()

    return True


def continue_render():

    # Prepare for renders
    clear_render_folder()
    save_object_materials()
    # Set materials opaque for beauty and depth passes
    set_object_materials_opaque()

    # Render all required passes
    render_all_passes()

    # Reset settings set for renders
    reset_object_materials()
    clean_up_files()

    return None


def render_all_passes():
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

    # Render unmodified image
    render_beauty_pass()
    # Render depth image
    render_depth_pass()
    # Render mask image
    render_mask_pass()
    # Render outline image
    render_outline_pass()


#
def clear_render_folder():
    dir = os.path.dirname(os.path.dirname(__file__))
    folder_path = os.path.join(dir, "renders")

    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
        except Exception as e:
            print(f"Failed to delete {folder_path}: {e}")
    else:
        print(f"File {folder_path} does not exist")


#
def clean_up_files():
    bpy.data.images.remove(bpy.data.images["Render Result"])

    dir = os.path.dirname(os.path.dirname(__file__))
    folder_path = os.path.join(dir, "renders")

    if not os.path.exists(folder_path):
        return

    files_in_directory = os.listdir(folder_path)

    # Depth and outline files have numbers after them (0001, 0002, etc.)
    # Get the file that includes "depth" / "outline"
    depth_file = [f for f in files_in_directory if "depth" in f]
    outline_file = [f for f in files_in_directory if "outline" in f]

    render_mist = os.path.join(folder_path, "render_mist.png")
    render_edge = os.path.join(folder_path, "render_edge.png")
    render_depth = os.path.join(folder_path, depth_file[0])
    render_outline = os.path.join(folder_path, outline_file[0])

    render_depth_new = os.path.join(folder_path, "depth.png")
    render_outline_new = os.path.join(folder_path, "outline.png")

    if os.path.exists(render_mist):
        os.remove(render_mist)
    if os.path.exists(render_edge):
        os.remove(render_edge)
    if os.path.exists(render_depth):
        os.rename(render_depth, render_depth_new)
    if os.path.exists(render_outline):
        os.rename(render_outline, render_outline_new)
