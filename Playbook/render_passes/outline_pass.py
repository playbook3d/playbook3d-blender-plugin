import bpy
import os

original_settings = {}


# Save the current color management settings
def save_outline_settings():
    scene = bpy.context.scene
    view_layer = scene.view_layers["ViewLayer"]

    original_settings.clear()
    original_settings.update(
        {
            "background_color": bpy.data.worlds["World"]
            .node_tree.nodes["Background"]
            .inputs[0]
            .default_value,
            "freestyle": scene.render.use_freestyle,
            "freestyle_pass": view_layer.use_freestyle,
            "render_pass": view_layer.freestyle_settings.as_render_pass,
            "silhouette": view_layer.freestyle_settings.linesets.active.select_silhouette,
            "crease": view_layer.freestyle_settings.linesets.active.select_crease,
            "border": view_layer.freestyle_settings.linesets.active.select_border,
            "freestyle_color": bpy.data.linestyles["LineStyle"].color,
        }
    )


#
def set_outline_settings():
    scene = bpy.context.scene
    view_layer = scene.view_layers["ViewLayer"]

    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (
        0,
        0,
        0,
        1,
    )
    scene.render.use_freestyle = True
    view_layer.use_freestyle = True
    view_layer.freestyle_settings.as_render_pass = True
    view_layer.freestyle_settings.linesets.active.select_silhouette = True
    view_layer.freestyle_settings.linesets.active.select_crease = True
    view_layer.freestyle_settings.linesets.active.select_border = True
    bpy.data.linestyles["LineStyle"].color = (0, 0, 0)


#
def reset_outline_settings():
    scene = bpy.context.scene
    view_layer = scene.view_layers["ViewLayer"]

    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (
        original_settings["background_color"]
    )
    scene.render.use_freestyle = original_settings["freestyle"]
    view_layer.use_freestyle = original_settings["freestyle_pass"]
    view_layer.freestyle_settings.as_render_pass = original_settings["render_pass"]
    view_layer.freestyle_settings.linesets.active.select_crease = original_settings[
        "silhouette"
    ]
    view_layer.freestyle_settings.linesets.active.select_crease = original_settings[
        "crease"
    ]
    view_layer.freestyle_settings.linesets.active.select_crease = original_settings[
        "border"
    ]
    bpy.data.linestyles["LineStyle"].color = original_settings["freestyle_color"]


#
def render_outline_to_file():
    scene = bpy.context.scene
    render = scene.render

    dir = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(dir, "renders", "render_edge.png")
    render.filepath = output_path

    if scene.node_tree is None:
        scene.use_nodes = True

    node_tree = scene.node_tree
    nodes = node_tree.nodes
    links = node_tree.links

    nodes.clear()

    # Create necessary nodes
    render_layers_node = nodes.new(type="CompositorNodeRLayers")
    alpha_node = nodes.new(type="CompositorNodeAlphaOver")
    invert_node = nodes.new(type="CompositorNodeInvert")
    output_node = nodes.new(type="CompositorNodeOutputFile")

    # Connect nodes
    links.new(render_layers_node.outputs["Freestyle"], alpha_node.inputs[2])
    links.new(alpha_node.outputs[0], invert_node.inputs[1])
    links.new(invert_node.outputs[0], output_node.inputs[0])

    # Set output file path and format
    node_path = os.path.join(dir, "renders")
    output_node.base_path = bpy.path.abspath(node_path)  # Set to your desired path
    output_node.file_slots[0].path = "outline"
    output_node.format.file_format = "PNG"

    bpy.ops.render.render(write_still=True)

    # nodes.clear()


#
def render_outline_pass():
    save_outline_settings()
    set_outline_settings()
    render_outline_to_file()
    reset_outline_settings()
