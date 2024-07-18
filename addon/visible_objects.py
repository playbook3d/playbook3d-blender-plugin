import bpy
from .utilities import material_props, create_rgb_material

visible_objects = []

original_materials = {}


# Get all mesh objects in the scene
def set_visible_objects():
    visible_objects.clear()
    for obj in bpy.data.objects:
        if obj.visible_get() and obj.type == "MESH":
            visible_objects.append(obj)


# Set the given materials to the object
def set_materials(obj, materials):
    if obj.type == "MESH":
        obj.data.materials.clear()
        for mat in materials:
            obj.data.materials.append(mat)


# Save the current object materials
def save_object_materials():
    for obj in visible_objects:
        original_materials[obj.name] = [slot.material for slot in obj.material_slots]


# Set the current object materials to a given preset
def set_object_materials():
    for obj in visible_objects:
        set_materials(
            obj, [create_rgb_material(name, color) for name, color in material_props]
        )


# Reset object materials to their originals
def reset_object_materials():
    for obj in visible_objects:
        set_materials(obj, original_materials[obj.name])
