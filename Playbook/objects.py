import bpy

visible_objects: list[bpy.types.Object] = []

hidden_objects: list[bpy.types.Object] = []

# Objects that are part of each mask
mask_objects: dict[str, list[str]] = {
    "MASK1": [],
    "MASK2": [],
    "MASK3": [],
    "MASK4": [],
    "MASK5": [],
    "MASK6": [],
    "MASK7": [],
}
