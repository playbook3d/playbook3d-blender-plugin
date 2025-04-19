
import bpy
from ..objects.objects import visible_objects, mask_objects
from ..objects.object_properties import ObjectProperties
from ..objects.object_utilities import mask_rgb_colors
from ..utilities.file_utilities import get_filepath
from ..properties.mask_properties import get_slot_for_object

original_settings = {}
original_object_properties = {}

def get_mask_materials():
    materials = {}
    for i in range(1, 9):
        name = f"SLOT_{i}"
        if name not in bpy.data.materials:
            mat = bpy.data.materials.new(name=name)
            mat.use_nodes = False
        else:
            mat = bpy.data.materials[name]
        color = mask_rgb_colors.get(name)
        if color:
            mat.diffuse_color = (*color[:3], 1.0)
        materials[name] = mat
    return materials

def save_mask_settings():
    scene = bpy.context.scene
    original_settings.clear()
    original_settings.update({
        "render_engine": scene.render.engine,
        "object_index": bpy.context.window.view_layer.use_pass_object_index,
        "display_device": scene.display_settings.display_device,
        "view_transform": scene.view_settings.view_transform,
        "look": scene.view_settings.look,
        "exposure": scene.view_settings.exposure,
        "gamma": scene.view_settings.gamma,
        "sequencer": scene.sequencer_colorspace_settings.name,
        "user_curves": scene.view_settings.use_curve_mapping,
        "file_format": scene.render.image_settings.file_format,
        "film_transparent": scene.render.film_transparent,
        "color_mode": scene.render.image_settings.color_mode,
        "color_depth": scene.render.image_settings.color_depth,
    })

def set_mask_settings():
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 1
    scene.render.image_settings.file_format = 'PNG'
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
    scene.render.image_settings.color_depth = "8"

def reset_mask_settings():
    scene = bpy.context.scene
    for k, v in original_settings.items():
        if k == "object_index":
            bpy.context.window.view_layer.use_pass_object_index = v
        elif hasattr(scene.render, k):
            setattr(scene.render, k, v)
        elif hasattr(scene.view_settings, k):
            setattr(scene.view_settings, k, v)
        elif hasattr(scene.display_settings, k):
            setattr(scene.display_settings, k, v)
        elif k == "sequencer":
            scene.sequencer_colorspace_settings.name = v
    scene = bpy.context.scene
    scene.render.engine = original_settings["render_engine"]
    scene.render.image_settings.color_mode = original_settings["color_mode"]
    scene.render.image_settings.file_format = original_settings["file_format"]
    scene.render.film_transparent = original_settings["film_transparent"]

def create_mask_compositing():
    scene = bpy.context.scene
    scene.use_nodes = True
    tree = scene.node_tree
    nodes = tree.nodes
    links = tree.links
    nodes.clear()

    render_layers = nodes.new(type="CompositorNodeRLayers")
    composite = nodes.new(type="CompositorNodeComposite")

    mix_chain = None
    for i, mask in enumerate(sorted(mask_objects.keys())):
        objs = mask_objects[mask]
        if not objs:
            continue

        try:
            index = int(mask[-1])
        except:
            index = 8

        color = mask_rgb_colors.get(mask, (1, 0, 0, 1))

        id_mask = nodes.new(type="CompositorNodeIDMask")
        id_mask.index = index
        links.new(render_layers.outputs["IndexOB"], id_mask.inputs["ID value"])

        color_mix = nodes.new(type="CompositorNodeMixRGB")
        color_mix.blend_type = "MULTIPLY"
        color_mix.inputs[2].default_value = color
        links.new(id_mask.outputs["Alpha"], color_mix.inputs[1])

        if mix_chain is None:
            mix_chain = color_mix
        else:
            new_mix = nodes.new(type="CompositorNodeMixRGB")
            new_mix.blend_type = "ADD"
            links.new(mix_chain.outputs["Image"], new_mix.inputs[1])
            links.new(color_mix.outputs["Image"], new_mix.inputs[2])
            mix_chain = new_mix

    if mix_chain:
        links.new(mix_chain.outputs["Image"], composite.inputs["Image"])

def render_mask_as_image():
    filepath = get_filepath("renders/mask.png")
    render_to_path(filepath)

def render_mask_as_sequence():
    capture_count = bpy.context.scene.render_properties.capture_count
    filepath = get_filepath(f"renders/mask_zip/mask_{capture_count:03}.png")
    render_to_path(filepath)

def render_to_path(filepath: str):
    bpy.context.scene.render.filepath = filepath
    create_mask_compositing()
    if bpy.context.scene.camera:
        bpy.ops.render.render(write_still=True)
    else:
        print("No camera found!")

def save_object_properties():
    original_object_properties.clear()
    mats = get_mask_materials()

    for obj in visible_objects:
        # ✅ Safety check: make sure the object still exists and is valid
        if not obj or obj.name not in bpy.data.objects:
            continue
        try:
            original_object_properties[obj.name] = ObjectProperties(obj.visible_shadow, obj.pass_index)
            obj.visible_shadow = False

            if obj.type == 'MESH':
                slot = get_slot_for_object(obj)
                obj.active_material = mats.get(slot) or mats.get("SLOT_1")
        except ReferenceError:
            print(f"⚠️ Skipped deleted object: {obj.name}")
            continue

def set_object_indeces():
    visible_objects_dict = {obj.name: obj for obj in bpy.context.visible_objects}
    mats = get_mask_materials()
    for mask, mask_objs in mask_objects.items():
        if mask not in mask_rgb_colors:
            mask_objs.clear()
            continue
        for obj_name in mask_objs:
            if obj_name in visible_objects_dict:
                obj = visible_objects_dict[obj_name]
                obj.pass_index = int(mask[-1])
                if obj.type == 'MESH':
                    slot = get_slot_for_object(obj)
                    obj.active_material = mats.get(slot) or mats.get("SLOT_1")
                visible_objects_dict.pop(obj_name)

    for obj in visible_objects_dict.values():
        obj.pass_index = 8
        if obj.type == 'MESH':
            slot = get_slot_for_object(obj)
            obj.active_material = mats.get(slot) or mats.get("SLOT_1")

def reset_object_properties():
    mats = get_mask_materials()
    for obj in visible_objects:
        props = original_object_properties.get(obj.name)
        if props:
            obj.visible_shadow = props.visible_shadow
            obj.pass_index = props.pass_index
        if obj.type == 'MESH':
            slot = get_slot_for_object(obj)
            obj.active_material = mats.get(slot) or mats.get("SLOT_1")

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
