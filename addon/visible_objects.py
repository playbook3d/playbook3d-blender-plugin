import bpy
from .utilities import create_rgb_material
from .objects import visible_objects, mask_objects

original_materials: dict[str, bpy.types.Material] = {}

material_props: dict[str, tuple[str, tuple]] = {
    "MASK1": ("YELLOW", (1, 0.8148, 0.0018, 1)),
    "MASK2": ("BLUE", (0.0044, 0.2051, 0.7378, 1)),
    "MASK3": ("TEAL", (0.1912, 0.6795, 0.7083, 1)),
    "MASK4": ("VIOLET", (0.0006, 0, 0.0242, 1)),
    "MASK5": ("GREEN", (0, 0.3419, 0.0844, 1)),
    "MASK6": ("PINK", (1, 0.15, 0.6239, 1)),
    "MASK7": ("ORANGE", (1, 0.2423, 0.0273, 1)),
    "CATCHALL": ("RED", (0.723, 0, 0, 1)),
}

color_hex: dict[str, str] = {
    "MASK1": "#ffe906",
    "MASK2": "#0e7ddf",
    "MASK3": "#79d7db",
    "MASK4": "#02002b",
    "MASK5": "#009e52",
    "MASK6": "#ff6ccf",
    "MASK7": "#ff872e",
}


# Set the given materials to the object
def set_materials(obj: bpy.types.Object, materials: list[bpy.types.Material]):
    obj.data.materials.clear()
    for mat in materials:
        obj.data.materials.append(mat)


# Save the current object materials
def save_object_materials():
    for obj in visible_objects:
        original_materials[obj.name] = [slot.material for slot in obj.material_slots]

    # Save background color
    original_materials["background"] = (
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value
    )


# Set the current object materials to a given preset
def set_object_materials():
    background_mask = None
    visible_objects_dict = {obj.name: obj for obj in visible_objects}

    # Get the mask that has the world background, if any
    for mask, objs in mask_objects.items():
        if "Background" in objs:
            background_mask = mask
            break

    # Set objects in masks to their respective material colors
    for mask, mask_objs in mask_objects.items():
        for mask_obj in mask_objs:
            print(f"Mask: {mask}, Object: {mask_obj}")
            if mask_obj == "Background":
                bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[
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
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[
            0
        ].default_value = material_props["CATCHALL"][1]


# Reset object materials to their originals
def reset_object_materials():
    for obj in visible_objects:
        set_materials(obj, original_materials[obj.name])

    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (
        original_materials["background"]
    )
