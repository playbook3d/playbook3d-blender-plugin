import bpy
import os
from ..utilities.file_utilities import get_filepath

original_settings = {}


# Save the current color management settings
def save_outline_settings():
    global original_settings

    scene = bpy.context.scene
    view_layers = bpy.context.view_layer

    if not scene.world:
        scene.world = bpy.data.worlds["World"]

    original_settings.clear()
    original_settings.update(
        {
            "z_pass": view_layers.use_pass_z,
            "normal_pass": view_layers.use_pass_normal,
            "position_pass": view_layers.use_pass_position,
        }
    )


#
def set_outline_settings():
    view_layer = bpy.context.view_layer

    view_layer.use_pass_z = True
    view_layer.use_pass_normal = True
    view_layer.use_pass_position = True


#
def reset_outline_settings():
    global original_settings

    view_layer = bpy.context.view_layer
    view_layer.use_pass_z = original_settings["z_pass"]
    view_layer.use_pass_normal = original_settings["normal_pass"]
    view_layer.use_pass_position = original_settings["position_pass"]


#
def render_outline_to_file():
    scene = bpy.context.scene
    render = scene.render

    output_path = get_filepath("renders/outline.png")
    render.filepath = output_path

    create_outline_compositing()

    bpy.ops.render.render(write_still=True)


#
def create_outline_compositing():
    scene = bpy.context.scene

    if not scene.use_nodes:
        scene.use_nodes = True

    node_tree = scene.node_tree
    nodes = node_tree.nodes
    links = node_tree.links

    nodes.clear()

    # Create necessary nodes
    render_layers_node = nodes.new(type="CompositorNodeRLayers")
    normalize_node = nodes.new(type="CompositorNodeNormalize")

    sobel_node1 = nodes.new(type="CompositorNodeFilter")
    sobel_node1.filter_type = "SOBEL"
    sobel_node2 = nodes.new(type="CompositorNodeFilter")
    sobel_node2.filter_type = "SOBEL"
    sobel_node3 = nodes.new(type="CompositorNodeFilter")
    sobel_node3.filter_type = "SOBEL"

    add_node1 = nodes.new(type="CompositorNodeMixRGB")
    add_node1.blend_type = "ADD"
    add_node2 = nodes.new(type="CompositorNodeMixRGB")
    add_node2.blend_type = "ADD"

    color_ramp_node = nodes.new(type="CompositorNodeValToRGB")
    color_ramp_node.color_ramp.elements[0].position = 0.999

    output_node = nodes.new(type="CompositorNodeComposite")

    # Connect nodes
    # Depth pass
    links.new(render_layers_node.outputs["Depth"], normalize_node.inputs["Value"])
    links.new(normalize_node.outputs["Value"], sobel_node1.inputs["Image"])
    links.new(sobel_node1.outputs["Image"], add_node1.inputs[1])

    # Normal pass
    links.new(render_layers_node.outputs["Normal"], sobel_node2.inputs["Image"])
    links.new(sobel_node2.outputs["Image"], add_node1.inputs[2])

    # Position pass
    links.new(render_layers_node.outputs["Position"], sobel_node3.inputs["Image"])
    links.new(sobel_node3.outputs["Image"], add_node2.inputs[2])

    links.new(add_node1.outputs["Image"], add_node2.inputs[1])
    links.new(add_node2.outputs["Image"], color_ramp_node.inputs["Fac"])
    links.new(color_ramp_node.outputs["Image"], output_node.inputs["Image"])


#
def render_outline_pass():
    save_outline_settings()
    set_outline_settings()
    render_outline_to_file()
    reset_outline_settings()
