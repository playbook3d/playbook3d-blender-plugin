import bpy
from bpy.utils import register_class, unregister_class
from bpy.types import Operator
from ..objects import mask_objects


# Add a mask to the mask list
class MaskListAddItem(Operator):
    bl_idname = "list.add_mask_item"
    bl_label = ""

    def execute(self, context):
        mask_len = len(context.scene.mask_list)

        if mask_len == 7:
            return {"CANCELLED"}

        item = context.scene.mask_list.add()
        item.name = f"Mask {mask_len + 1}"

        context.scene.mask_list_index = len(context.scene.mask_list) - 1

        return {"FINISHED"}


# Remove the last mask from the mask list
class MaskListRemoveItem(Operator):
    bl_idname = "list.remove_mask_item"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return context.scene.mask_list

    def execute(self, context):
        mask_list = context.scene.mask_list
        index = len(context.scene.mask_list) - 1

        mask_list.remove(index)

        if len(mask_list) > 0:
            context.scene.mask_list_index = 0
        else:
            context.scene.mask_list_index = -1

        return {"FINISHED"}


# Add the currently selected object (in the viewport) to the
# currently selected mask
class MaskObjectListAddItem(Operator):
    bl_idname = "list.add_mask_object_item"
    bl_label = ""

    def execute(self, context):
        mask_index = context.scene.mask_list_index
        mask = getattr(context.scene, f"mask_properties{mask_index + 1}")

        # No object selected in the object dropdown
        if mask.object_dropdown == "NONE":
            obj = bpy.context.active_object

            # There is no currently selected object or the currently
            # selected object is not a mesh
            if not obj or obj.type != "MESH":
                return {"CANCELLED"}

            obj_name = obj.name

        elif mask.object_dropdown == "BACKGROUND":
            obj_name = "Background"

        else:
            obj_name = mask.object_dropdown

        # The currently selected item is already part of the list
        if any(item.name == obj_name for item in mask.mask_objects):
            return {"CANCELLED"}

        item = mask.mask_objects.add()
        item.name = obj_name

        mask_objects[f"MASK{mask_index + 1}"].append(item.name)

        return {"FINISHED"}


# Remove the currently selected index in the list from the
# currently selected mask
class MaskObjectListRemoveItem(Operator):
    bl_idname = "list.remove_mask_object_item"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        mask_index = context.scene.mask_list_index
        return getattr(context.scene, f"mask_properties{mask_index + 1}")

    def execute(self, context):
        mask_index = context.scene.mask_list_index
        mask = getattr(context.scene, f"mask_properties{mask_index + 1}")

        if not mask.mask_objects:
            return {"CANCELLED"}

        index = (
            mask.object_list_index
            if mask.object_list_index != -1
            # If no object list index is selected but items exists in the list
            # delete the last object
            else len(mask.mask_objects) - 1
        )

        mask.mask_objects.remove(index)
        mask_objects[f"MASK{mask_index + 1}"].pop(index)

        mask.object_list_index = 0 if mask.mask_objects else -1

        return {"FINISHED"}


# Clear all the objects from the currently selected mask
class MaskObjectListClearItems(Operator):
    bl_idname = "list.clear_mask_object_list"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        mask_index = context.scene.mask_list_index
        return getattr(context.scene, f"mask_properties{mask_index + 1}")

    def execute(self, context):
        mask_index = context.scene.mask_list_index
        mask = getattr(context.scene, f"mask_properties{mask_index + 1}")

        mask.mask_objects.clear()

        mask.object_list_index = -1

        return {"FINISHED"}


classes = [
    MaskListAddItem,
    MaskListRemoveItem,
    MaskObjectListAddItem,
    MaskObjectListRemoveItem,
    MaskObjectListClearItems,
]


def register():
    global classes
    for cls in classes:
        register_class(cls)


def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)
