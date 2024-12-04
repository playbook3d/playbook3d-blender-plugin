import bpy
from bpy.props import (
    PointerProperty,
    IntProperty,
    StringProperty,
    EnumProperty,
    CollectionProperty,
)
from bpy.types import Scene, PropertyGroup
from bpy.utils import register_class, unregister_class
from ..objects.visible_objects import set_visible_objects
from ..objects.objects import visible_objects, mask_objects
from .lists.lists import MaskObjectListItem

NUM_MASKS_ALLOWED = 7


#
class MaskProperties(PropertyGroup):
    #
    def update_mask_name(self, context):
        masks = context.scene.mask_list
        mask_index = context.scene.mask_list_index

        masks[mask_index].name = self.mask_name

    # Return a list of the available objects in the scene
    def update_object_dropdown(self, context):
        set_visible_objects(context)
        items = [(obj.name, obj.name, "") for obj in visible_objects]

        # None option
        items.insert(0, ("NONE", "Select an object from the scene", ""))

        # Objects currently in masks
        object_names = [tup for obj_list in mask_objects.values() for tup in obj_list]

        items = [item for item in items if item[0] not in object_names]

        # More than one option available
        if len(items) > 1:
            # Add all option
            items.insert(1, ("ADDALL", "Add All", ""))

        # Background not part of any mask
        if "Background" not in object_names:
            # Background option
            items.insert(1, ("BACKGROUND", "Background", ""))

        return items

    mask_name: StringProperty(
        name="", update=lambda self, context: self.update_mask_name(context)
    )
    mask_objects: CollectionProperty(type=MaskObjectListItem, name="")
    object_list_index: IntProperty(name="", default=-1)
    object_dropdown: EnumProperty(
        name="",
        items=update_object_dropdown,
    )


#
def reset_properties():
    # Reset properties
    scene = bpy.context.scene

    scene.error_message = ""

    for i in range(NUM_MASKS_ALLOWED):
        mask_props = getattr(scene, f"mask_properties{i + 1}")
        mask_props.mask_objects.clear()


classes = [
    MaskProperties,
]


def register():
    register_class(MaskProperties)

    for i in range(NUM_MASKS_ALLOWED):
        setattr(
            Scene,
            f"mask_properties{i + 1}",
            PointerProperty(type=MaskProperties),
        )


def unregister():
    reset_properties()

    unregister_class(MaskProperties)

    for i in range(NUM_MASKS_ALLOWED):
        delattr(Scene, f"mask_properties{i + 1}")
