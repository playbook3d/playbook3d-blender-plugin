import bpy
from ..objects.objects import visible_objects, mask_objects
from ..objects.object_properties import ObjectProperties
from ..objects.object_utilities import mask_rgb_colors
from ..utilities.file_utilities import get_filepath

original_settings = {}

original_object_properties: dict[ObjectProperties] = {}


# Save the current color management settings
def save_mask_settings():
    scene = bpy.context.scene

    original_settings.clear()
    original_settings.update(
        {
            "render_engine": scene.render.engine,
            "object_index": bpy.context.window.view_layer.use_pass_object_index,
            "display_device": scene.display_settings.display_device,
            "view_transform": scene.view_settings.view_transform,
            "look": scene.view_settings.look,
            "exposure": scene.view_settings.exposure,
            "gamma": scene.view_settings.gamma,
            "sequencer": scene.sequencer_colorspace_settings.name,
            "user_curves": scene.view_settings.use_curve_mapping,
            "film_transparent": scene.render.film_transparent,
            "color_mode": scene.render.image_settings.color_mode,
            "color_depth": scene.render.image_settings.color_depth,
        }
    )


# Prepare the color management settings for render
def set_mask_settings():
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 1
    bpy.context.window.view_layer.use_pass_object_index = True
    scene.display_settings.display_device = "sRGB"
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = 0
    scene.view_settings.gamma = 1
    scene.sequencer_colorspace_settings.name = "sRGB"
    scene.view_settings.use_curve_mapping = False
    scene.render.film_transparent = True
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "16"


# Reset the color management settings to their previous values
def reset_mask_settings():
    scene = bpy.context.scene
    scene.render.engine = original_settings["render_engine"]
    bpy.context.window.view_layer.use_pass_object_index = original_settings[
        "object_index"
    ]
    scene.display_settings.display_device = original_settings["display_device"]
    scene.view_settings.view_transform = original_settings["view_transform"]
    scene.view_settings.look = original_settings["look"]
    scene.view_settings.exposure = original_settings["exposure"]
    scene.view_settings.gamma = original_settings["gamma"]
    scene.sequencer_colorspace_settings.name = original_settings["sequencer"]
    scene.view_settings.use_curve_mapping = original_settings["user_curves"]
    scene.render.film_transparent = original_settings["film_transparent"]
    scene.render.image_settings.color_mode = original_settings["color_mode"]
    scene.render.image_settings.color_depth = original_settings["color_depth"]


#
def render_mask_as_image():
    filepath = get_filepath("renders/mask.png")
    render_to_path(filepath)


#
def render_mask_as_sequence():
    capture_count = bpy.context.scene.render_properties.capture_count
    filepath = get_filepath(f"renders/mask_zip/mask_{capture_count:03}.png")
    render_to_path(filepath)


#
def render_to_path(filepath: str):
    scene = bpy.context.scene
    render = scene.render

    render.filepath = filepath

    create_mask_compositing()

    if scene.camera:
        bpy.ops.render.render(write_still=True)
    else:
        print("No active camera found in the scene")


#
def create_mask_compositing():
    scene = bpy.context.scene

    if not scene.use_nodes:
        scene.use_nodes = True

    node_tree = scene.node_tree
    nodes = node_tree.nodes
    links = node_tree.links

    nodes.clear()

    # Create nodes
    render_layers_node = nodes.new(type="CompositorNodeRLayers")

    create_id_mask_nodes(nodes, links, render_layers_node)

    mask_nodes = create_idmask_nodes(nodes, links, render_layers_node)

    mix_node = nodes.new(type="CompositorNodeMixRGB")
    mix_node.blend_type = "ADD"
    mix_node.inputs[2].default_value = (0, 0, 0, 0)

    # Background nodes
    background_mask_name = "CATCHALL"
    for mask, objs in mask_objects.items():
        if "Background" in objs:
            background_mask_name = mask
    background_node = create_background_nodes(
        nodes, links, render_layers_node, background_mask_name
    )

    output_node = nodes.new("CompositorNodeComposite")

    # Create links
    # Mask links
    links.new(mask_nodes[0].outputs["Image"], mix_node.inputs[1])

    for mask_node in mask_nodes[1:]:
        new_mix_node = nodes.new("CompositorNodeMixRGB")
        new_mix_node.blend_type = "ADD"

        links.new(mix_node.outputs["Image"], new_mix_node.inputs[1])
        links.new(mask_node.outputs["Image"], new_mix_node.inputs[2])

        mix_node = new_mix_node

    # Background links
    links.new(mix_node.outputs["Image"], background_node.inputs[2])
    links.new(background_node.outputs["Image"], output_node.inputs["Image"])


#
def create_idmask_nodes(nodes, links, render_layers_node):
    mask_nodes = []

    # Catch-all node
    catchall_idmask_node = nodes.new(type="CompositorNodeIDMask")
    catchall_idmask_node.index = 8

    catchall_mix_node = nodes.new(type="CompositorNodeMixRGB")
    catchall_mix_node.blend_type = "MULTIPLY"
    catchall_mix_node.inputs[2].default_value = mask_rgb_colors["CATCHALL"]

    links.new(
        render_layers_node.outputs["IndexOB"], catchall_idmask_node.inputs["ID value"]
    )
    links.new(catchall_idmask_node.outputs["Alpha"], catchall_mix_node.inputs[1])

    mask_nodes.append(catchall_mix_node)

    for mask, objs in mask_objects.items():

        # No objects in this mask. Ignore
        if not objs:
            continue

        idmask_node = nodes.new(type="CompositorNodeIDMask")
        idmask_node.index = int(mask[-1])

        mask_node = nodes.new(type="CompositorNodeMixRGB")
        mask_node.blend_type = "MULTIPLY"
        mask_node.inputs[2].default_value = mask_rgb_colors[mask]

        links.new(render_layers_node.outputs["IndexOB"], idmask_node.inputs["ID value"])
        links.new(idmask_node.outputs["Alpha"], mask_node.inputs[1])

        mask_nodes.append(mask_node)

    return mask_nodes


#
def create_id_mask_nodes(nodes, links, render_layers_node):
    idmask_node = nodes.new(type="CompositorNodeIDMask")
    idmask_node.index = 0

    alpha_over_node = nodes.new(type="CompositorNodeAlphaOver")

    links.new(render_layers_node.outputs["IndexOB"], idmask_node.inputs["ID value"])
    links.new(idmask_node.outputs["Alpha"], alpha_over_node.inputs["Fac"])

    return alpha_over_node


#
def create_background_nodes(nodes, links, render_layers_node, mask_name: str):
    alpha_over_node = nodes.new(type="CompositorNodeAlphaOver")
    alpha_over_node.inputs[1].default_value = mask_rgb_colors[mask_name]

    links.new(render_layers_node.outputs["Alpha"], alpha_over_node.inputs["Fac"])

    return alpha_over_node


#
def save_object_properties():
    original_object_properties.clear()

    for obj in visible_objects:
        original_object_properties[obj.name] = ObjectProperties(
            obj.visible_shadow, obj.pass_index
        )

        obj.visible_shadow = False


#
def set_object_indeces():
    visible_objects_dict = {obj.name: obj for obj in visible_objects}

    for mask, mask_objs in mask_objects.items():
        for mask_obj in mask_objs:
            print(f"Mask: {mask}, Object: {mask_obj}")

            # Background color is set in compositing
            if mask_obj == "Background":
                continue

            if mask_obj in visible_objects_dict:
                obj = visible_objects_dict[mask_obj]
                obj.pass_index = int(mask[-1])  # Index of mask

                visible_objects_dict.pop(mask_obj)

    # All remaining visible objects are set in the catch-all mask
    for obj in visible_objects_dict.values():
        obj.pass_index = 8  # Catch-all index


#
def reset_object_properties():
    for obj in visible_objects:
        obj.visible_shadow = original_object_properties[obj.name].visible_shadow
        obj.pass_index = original_object_properties[obj.name].pass_index


#
def render_mask_pass(is_image: bool):
    save_mask_settings()
    save_object_properties()

    set_mask_settings()
    set_object_indeces()

    if is_image:
        render_mask_as_image()
    else:
        render_mask_as_sequence()

    reset_mask_settings()
    reset_object_properties()
