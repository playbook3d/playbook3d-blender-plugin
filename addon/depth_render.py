import bpy
import os

original_settings = {}


#
def save_depth_settings():
    scene = bpy.context.scene

    original_settings.clear()
    original_settings.update(
        {
            "use_pass_z": scene.view_layers["ViewLayer"].use_pass_z,
        }
    )


#
def set_depth_settings():
    scene = bpy.context.scene

    scene.view_layers["ViewLayer"].use_pass_z = True


#
def reset_depth_settings():
    scene = bpy.context.scene

    scene.view_layers["ViewLayer"].use_pass_z = original_settings["use_pass_z"]


#
def render_depth_to_file():
    scene = bpy.context.scene
    render = scene.render

    dir = os.path.dirname(__file__)

    output_path = os.path.join(dir, "renders", "render_mist.png")
    render.filepath = output_path

    if scene.node_tree is None:
        scene.use_nodes = True

    node_tree = scene.node_tree
    nodes = node_tree.nodes
    links = node_tree.links

    nodes.clear()

    # Render settings
    render.use_compositing = True

    # Create necessary nodes
    render_layers_node = nodes.new(type="CompositorNodeRLayers")
    normal_node = nodes.new(type="CompositorNodeNormalize")
    color_node = nodes.new(type="CompositorNodeValToRGB")
    rgb_node = nodes.new(type="CompositorNodeCurveRGB")
    output_node = nodes.new(type="CompositorNodeOutputFile")

    # Set color ramp node
    color_ramp = color_node.color_ramp
    color_ramp.elements[0].color = (0.87977, 0.879584, 0.879559, 1)  # Set to 0xF1F1F1
    color_ramp.elements[1].color = (0, 0, 0, 1)  # Set to 0x000000

    # Set RGB curves node
    curve = rgb_node.mapping.curves[3]  # Adding points to C channel
    curve.points.new(0.606, 0.131)
    curve.points.new(0.811, 0.256)
    curve.points.new(0.939, 0.450)

    # Connect nodes
    links.new(render_layers_node.outputs["Depth"], normal_node.inputs[0])
    links.new(normal_node.outputs[0], color_node.inputs[0])
    links.new(color_node.outputs[0], rgb_node.inputs["Image"])
    links.new(rgb_node.outputs[0], output_node.inputs[0])

    # Set output file path and format
    node_path = os.path.join(dir, "renders")
    output_node.base_path = bpy.path.abspath(node_path)  # Set to your desired path
    output_node.file_slots[0].path = "render_depth"
    output_node.format.file_format = "PNG"

    bpy.ops.render.render(write_still=True)

    # nodes.clear()
