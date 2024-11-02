import bpy
import os
from ..utilities.utilities import get_parent_filepath

original_settings = {}


# Save the current color management settings
def save_outline_settings():
    scene = bpy.context.scene
    view_layer = scene.view_layers["ViewLayer"]

    original_settings.clear()
    original_settings.update(
        {
            "background_color": bpy.data.worlds["World"]
            .node_tree.nodes["RGB"]
            .outputs[0]
            .default_value,
            "freestyle": scene.render.use_freestyle,
            "freestyle_pass": view_layer.use_freestyle,
            "render_pass": view_layer.freestyle_settings.as_render_pass,
            "freestyle_color": bpy.data.linestyles["LineStyle"].color,
        }
    )
    if view_layer.freestyle_settings.linesets.active:
        original_settings.update(
            {
                "silhouette": view_layer.freestyle_settings.linesets.active.select_silhouette,
                "crease": view_layer.freestyle_settings.linesets.active.select_crease,
                "border": view_layer.freestyle_settings.linesets.active.select_border,
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

    if not view_layer.freestyle_settings.linesets.active:
        view_layer.freestyle_settings.linesets.new("LineSet")

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

    if "silhouette" in original_settings:
        view_layer.freestyle_settings.linesets.active.select_crease = original_settings[
            "silhouette"
        ]
    if "crease" in original_settings:
        view_layer.freestyle_settings.linesets.active.select_crease = original_settings[
            "crease"
        ]
    if "border" in original_settings:
        view_layer.freestyle_settings.linesets.active.select_crease = original_settings[
            "border"
        ]
    bpy.data.linestyles["LineStyle"].color = original_settings["freestyle_color"]


#
def render_outline_to_file():
    scene = bpy.context.scene
    render = scene.render

    output_path = get_parent_filepath("outline.png", "renders")
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
    alpha_node = nodes.new(type="CompositorNodeAlphaOver")
    invert_node = nodes.new(type="CompositorNodeInvert")
    output_node = nodes.new(type="CompositorNodeComposite")

    # Connect nodes
    links.new(render_layers_node.outputs["Freestyle"], alpha_node.inputs[2])
    links.new(alpha_node.outputs[0], invert_node.inputs[1])
    links.new(invert_node.outputs[0], output_node.inputs["Image"])


#
def render_outline_pass():
    save_outline_settings()
    set_outline_settings()
    render_outline_to_file()
    reset_outline_settings()
