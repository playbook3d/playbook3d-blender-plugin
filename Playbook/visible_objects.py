import bpy
from .utilities.utilities import create_rgb_material
from .objects import visible_objects, mask_objects, hidden_objects

original_materials: dict[str, bpy.types.Material] = {}
background_color = None

material_props: dict[str, tuple[str, tuple]] = {
    "MASK1": ("YELLOW", (1, 0.8148, 0.0018, 1)),
    "MASK2": ("BLUE", (0.0015, 0.2501, 0.6724, 1)),
    "MASK3": ("TEAL", (0.3614, 0.6583, 0.6653, 1)),
    "MASK4": ("VIOLET", (0, 0, 0.0080, 1)),
    "MASK5": ("GREEN", (0, 0.4179, 0.0976, 1)),
    "MASK6": ("PINK", (0.8715, 0.2307, 0.6239, 1)),
    "MASK7": ("ORANGE", (0.8551, 0.3419, 0.0482, 1)),
    "CATCHALL": ("RED", (0.7914, 0, 0.0037, 1)),
}

color_hex: dict[str, str] = {
    "MASK1": "#ffe906",
    "MASK2": "#0589d6",
    "MASK3": "#a2d4d5",
    "MASK4": "#000016",
    "MASK5": "#00ad58",
    "MASK6": "#f084cf",
    "MASK7": "#ee9e3e",
}

allowed_obj_types = ["MESH", "FONT", "META", "SURFACE"]


# Get all visible objects in the scene
def set_visible_objects(context):
    visible_objects.clear()
    for obj in context.scene.objects:

        if obj.hide_render:
            continue

        # Object is not visible. Ignore
        if obj.hide_get():
            obj.hide_render = True
            hidden_objects.append(obj)
            continue

        if obj.type in allowed_obj_types:
            visible_objects.append(obj)


# Set the given materials to the object
def set_materials(obj: bpy.types.Object, materials: list[bpy.types.Material]):
    obj.data.materials.clear()
    for mat in materials:
        obj.data.materials.append(mat)


# Save the current object materials
def save_object_materials():
    for obj in visible_objects:
        original_materials[obj.name] = [slot.material for slot in obj.material_slots]

    if not bpy.context.scene.world.use_nodes:
        return

    # Save background color
    global background_color
    background_node = bpy.data.worlds["World"].node_tree.nodes["Background"]

    if background_node:
        background_color = tuple(background_node.inputs[0].default_value)


#
def set_object_materials_opaque():
    for obj in visible_objects:
        copied_materials = [slot.material.copy() for slot in obj.material_slots]
        obj.data.materials.clear()

        for mat in copied_materials:
            mat.blend_method = "OPAQUE"
            obj.data.materials.append(mat)


# Make the world background unreflective so the mask color is not reflected in the
# scene objects
def make_background_unreflective():
    world = bpy.context.scene.world

    if not world.use_nodes:
        world.use_nodes = True

    nodes = world.node_tree.nodes
    nodes.clear()

    light_path_node = nodes.new(type="ShaderNodeLightPath")
    rgb_node = nodes.new(type="ShaderNodeRGB")
    mix_node = nodes.new(type="ShaderNodeMixRGB")
    background_node = nodes.new(type="ShaderNodeBackground")
    world_output_node = nodes.new(type="ShaderNodeOutputWorld")

    links = world.node_tree.links
    light_path_output = (
        "Is Diffuse Ray" if bpy.app.version < (4, 2, 0) else "Is Glossy Ray"
    )
    links.new(light_path_node.outputs[light_path_output], mix_node.inputs["Fac"])
    links.new(rgb_node.outputs["Color"], mix_node.inputs["Color1"])
    links.new(mix_node.outputs["Color"], background_node.inputs["Color"])
    links.new(
        background_node.outputs["Background"], world_output_node.inputs["Surface"]
    )


#
def reset_background():
    global background_color

    world = bpy.context.scene.world
    nodes = world.node_tree.nodes
    nodes.clear()

    background_node = nodes.new(type="ShaderNodeBackground")
    world_output_node = nodes.new(type="ShaderNodeOutputWorld")

    links = world.node_tree.links
    links.new(
        background_node.outputs["Background"], world_output_node.inputs["Surface"]
    )
    background_node.inputs["Color"].default_value = background_color


# Set the current object materials to a given preset
def set_object_materials_for_mask_pass():
    background_mask = None
    visible_objects_dict = {obj.name: obj for obj in visible_objects}

    # Get the mask that has the world background, if any
    for mask, objs in mask_objects.items():
        if "Background" in objs:
            background_mask = mask
            break

    preserve_mask = (
        bpy.context.scene.retexture_properties.preserve_texture_mask_index + 1
    )

    # Set objects in masks to their respective material colors
    for mask, mask_objs in mask_objects.items():
        # Skip objects in the mask to be preserved
        if mask == f"MASK{preserve_mask}":
            for mask_obj in mask_objs:
                visible_objects_dict.pop(mask_obj)

            continue

        for mask_obj in mask_objs:
            print(f"Mask: {mask}, Object: {mask_obj}")
            if mask_obj == "Background":
                bpy.context.scene.world.node_tree.nodes["RGB"].outputs[
                    0
                ].default_value = material_props[mask][1]
            elif mask_obj in visible_objects_dict:
                set_materials(
                    visible_objects_dict[mask_obj],
                    [
                        create_rgb_material(
                            material_props[mask][0], material_props[mask][1]
                        )
                    ],
                )
                visible_objects_dict.pop(mask_obj)

    # All remaining visible objects are set in the catch-all mask
    catchall_mat = create_rgb_material(
        material_props["CATCHALL"][0], material_props["CATCHALL"][1]
    )
    for obj in visible_objects_dict.values():
        set_materials(obj, [catchall_mat])

    # Set the world background to the catch-call color if it was not part of a mask
    if not background_mask:
        bpy.context.scene.world.node_tree.nodes["RGB"].outputs[0].default_value = (
            material_props["CATCHALL"][1]
        )


# Reset object materials to their originals
def reset_object_materials():
    for obj in visible_objects:
        set_materials(obj, original_materials[obj.name])

    for obj in hidden_objects:
        obj.hide_render = False

    global background_color
    bpy.context.scene.world.node_tree.nodes["Background"].inputs[
        0
    ].default_value = background_color
