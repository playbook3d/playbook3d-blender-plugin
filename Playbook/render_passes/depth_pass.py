import bpy
from ..utilities.file_utilities import get_filepath

original_settings = {}


#
def save_depth_settings():
    scene = bpy.context.scene

    if not scene.world:
        scene.world = bpy.data.worlds["World"]

    original_settings.clear()
    original_settings.update(
        {
            "z_pass": bpy.context.view_layer.use_pass_z,
            "exposure": scene.view_settings.exposure,
            "gamma": scene.view_settings.gamma,
        }
    )


#
def set_depth_settings():
    scene = bpy.context.scene

    bpy.context.view_layer.use_pass_z = True
    scene.view_settings.exposure = 1
    scene.view_settings.gamma = 1


#
def reset_depth_settings():
    scene = bpy.context.scene

    bpy.context.view_layer.use_pass_z = original_settings["z_pass"]
    scene.view_settings.exposure = original_settings["exposure"]
    scene.view_settings.gamma = original_settings["gamma"]


#
def render_depth_to_file():
    scene = bpy.context.scene
    render = scene.render

    output_path = get_filepath("renders/depth.png")
    render.filepath = output_path

    create_depth_compositing()

    bpy.ops.render.render(write_still=True)


#
def create_depth_compositing():
    scene = bpy.context.scene

    if not scene.use_nodes:
        scene.use_nodes = True

    node_tree = scene.node_tree
    nodes = node_tree.nodes
    links = node_tree.links

    nodes.clear()

    # Create nodes
    render_layers_node = nodes.new(type="CompositorNodeRLayers")
    normalize_node = nodes.new(type="CompositorNodeNormalize")
    invert_node = nodes.new(type="CompositorNodeInvert")

    rgb_curve_node = nodes.new(type="CompositorNodeCurveRGB")
    curve = rgb_curve_node.mapping.curves[3]
    curve.points.new(0.944, 0.125)
    curve.points.new(0.956, 0.144)
    rgb_curve_node.mapping.update()

    output_node = nodes.new(type="CompositorNodeComposite")

    # Connect nodes
    links.new(render_layers_node.outputs["Depth"], normalize_node.inputs["Value"])
    links.new(normalize_node.outputs["Value"], invert_node.inputs["Fac"])
    links.new(invert_node.outputs[0], rgb_curve_node.inputs["Image"])
    links.new(rgb_curve_node.outputs["Image"], output_node.inputs["Image"])


#
def render_depth_pass():
    save_depth_settings()
    set_depth_settings()
    render_depth_to_file()
    reset_depth_settings()
