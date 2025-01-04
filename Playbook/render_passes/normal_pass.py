import bpy
from ..utilities.file_utilities import get_filepath


original_render_engine = ""
original_settings = {}


#
def save_normal_settings():
    global original_render_engine

    scene = bpy.context.scene

    original_render_engine = ""
    original_settings.clear()

    if scene.render.engine != "BLENDER_WORKBENCH":
        original_render_engine = scene.render.engine
    else:
        original_settings.update(
            {
                "lighting": scene.display.shading.light,
                "studio_light": scene.display.shading.studio_light,
                "transparent": scene.render.film_transparent,
            }
        )


#
def set_normal_settings():
    scene = bpy.context.scene

    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "MATCAP"
    scene.display.shading.studio_light = "check_normal+y.exr"
    scene.render.film_transparent = True


#
def reset_normal_settings():
    scene = bpy.context.scene

    if original_render_engine:
        scene.render.engine = original_render_engine
    elif original_settings:
        scene.display.shading.light = original_settings["lighting"]
        scene.display.shading.studio_light = original_settings["studio_light"]
        scene.render.film_transparent = original_settings["transparent"]


#
def create_normal_compositing():
    scene = bpy.context.scene

    if not scene.use_nodes:
        scene.use_nodes = True

    node_tree = scene.node_tree
    nodes = node_tree.nodes
    links = node_tree.links

    nodes.clear()

    render_layers_node = nodes.new(type="CompositorNodeRLayers")
    mix_node = nodes.new(type="CompositorNodeMixRGB")

    mix_add_node = nodes.new(type="CompositorNodeMixRGB")
    mix_add_node.blend_type = "ADD"
    mix_add_node.inputs[1].default_value = (0.0594798, 0.0112964, 0.520969, 1)
    mix_add_node.inputs[2].default_value = (0.566359, 0.048713, 0.828737, 1)

    box_mask_node = nodes.new(type="CompositorNodeBoxMask")
    box_mask_node.x = 1
    box_mask_node.y = 1
    box_mask_node.width = 0.7
    box_mask_node.height = 2

    blur_node = nodes.new(type="CompositorNodeBlur")
    blur_node.filter_type = "FAST_GAUSS"
    blur_node.size_x = 1000
    blur_node.size_y = 1000

    output_node = nodes.new(type="CompositorNodeComposite")

    links.new(render_layers_node.outputs["Image"], mix_node.inputs[2])
    links.new(render_layers_node.outputs["Alpha"], mix_node.inputs["Fac"])
    links.new(box_mask_node.outputs["Mask"], blur_node.inputs["Image"])
    links.new(blur_node.outputs["Image"], mix_add_node.inputs["Fac"])
    links.new(mix_add_node.outputs["Image"], mix_node.inputs[1])
    links.new(mix_node.outputs["Image"], output_node.inputs["Image"])


#
def render_normal_to_file():
    render = bpy.context.scene.render

    output_path = get_filepath("renders/normal.png")
    render.filepath = output_path

    create_normal_compositing()

    bpy.ops.render.render(write_still=True)


#
def render_normal_pass():
    save_normal_settings()
    set_normal_settings()
    render_normal_to_file()
    reset_normal_settings()
