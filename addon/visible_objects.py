import bpy
from .utilities import create_rgb_material
from .properties import visible_objects, mask_objects

original_materials = {}

material_props = {
    "MASK1": ("YELLOW", (1, 233 / 255, 6 / 255, 1)),
    "MASK2": ("BLUE", (14 / 255, 125 / 255, 223 / 255, 1)),
    "MASK3": ("TEAL", (121 / 255, 215 / 255, 219 / 255, 1)),
    "MASK4": ("VIOLET", (2 / 255, 0, 43 / 255, 1)),
    "MASK5": ("GREEN", (0, 158 / 255, 82 / 255, 1)),
    "MASK6": ("PINK", (1, 108 / 255, 207 / 255, 1)),
    "MASK7": ("ORANGE", (1, 135 / 255, 46 / 255, 1)),
    "CATCHALL": ("RED", (221 / 225, 0, 0, 1)),
}


# Set the given materials to the object
def set_materials(obj, materials):
    obj.data.materials.clear()
    for mat in materials:
        obj.data.materials.append(mat)


# Save the current object materials
def save_object_materials():
    for obj in visible_objects:
        original_materials[obj.name] = [slot.material for slot in obj.material_slots]


# Set the current object materials to a given preset
def set_object_materials():
    visible_objects_dict = {obj.name: obj for obj in visible_objects}

    for mask, mask_obj in mask_objects.items():
        if mask_obj and mask_obj in visible_objects_dict:
            set_materials(
                visible_objects_dict[mask_obj],
                [create_rgb_material(material_props[mask][0], material_props[mask][1])],
            )

            visible_objects_dict.pop(mask_obj)

    # All remaining visible objects are set in Mask 8
    for obj_name, obj in visible_objects_dict.items():
        set_materials(
            obj,
            [
                create_rgb_material(
                    material_props["CATCHALL"][0], material_props["CATCHALL"][1]
                )
            ],
        )


# Reset object materials to their originals
def reset_object_materials():
    for obj in visible_objects:
        set_materials(obj, original_materials[obj.name])
