import bpy
from bpy.utils import register_class, unregister_class
from bpy.types import Operator
from ..visible_objects import visible_objects
from ..objects import mask_objects

MAX_MASKS = 7


# Add a mask to the mask list
class MaskListAddItem(Operator):
    bl_idname = "list.add_mask_item"
    bl_label = ""
    bl_description = "Add mask"

    @classmethod
    def poll(cls, context):
        return len(context.scene.mask_list) < 7

    def execute(self, context):
        mask_len = len(context.scene.mask_list)

        # Reached max number of masks
        if mask_len == MAX_MASKS:
            return {"CANCELLED"}

        item = context.scene.mask_list.add()
        item.name = f"Mask {mask_len + 1}"

        context.scene.mask_list_index = len(context.scene.mask_list) - 1

        return {"FINISHED"}


# Remove the last mask from the mask list
class MaskListRemoveItem(Operator):
    bl_idname = "list.remove_mask_item"
    bl_label = ""
    bl_description = "Remove mask"

    @classmethod
    def poll(cls, context):
        if context.scene.mask_list_index == -1:
            return False
        else:
            return context.scene.mask_list

    def execute(self, context):
        mask_list = context.scene.mask_list

        mask_list.remove(context.scene.mask_list_index)

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
    bl_description = "Add object"

    @classmethod
    def poll(cls, context):
        selected_objects = [obj for obj in context.selected_objects]

        if selected_objects:
            for obj in selected_objects:

                if obj.type not in {"MESH", "FONT"}:
                    continue

                # Object is already part of a mask
                if any(obj.name in obj_list for obj_list in mask_objects.values()):
                    continue

                # At least one object can be added
                return True

            # No object can be added
            return False

        mask_index = context.scene.mask_list_index
        mask = getattr(context.scene, f"mask_properties{mask_index + 1}")

        # No object selected in the object dropdown
        return mask.object_dropdown != "NONE"

    def execute(self, context):
        mask_index = context.scene.mask_list_index
        mask = getattr(context.scene, f"mask_properties{mask_index + 1}")

        selected_objects = [obj for obj in context.selected_objects]
        # There exists at least one selected object
        if selected_objects:
            # At least one selected object was added to the mask
            if self.add_selected_objects(mask, mask_index, selected_objects):
                return {"FINISHED"}

        # No object selected in the object dropdown
        if mask.object_dropdown == "NONE":
            return {"CANCELLED"}

        elif mask.object_dropdown == "ADDALL":
            self.add_all_objects(mask, mask_index)
            return {"FINISHED"}

        elif mask.object_dropdown == "BACKGROUND":
            obj_name = "Background"

        else:
            obj_name = mask.object_dropdown

        # Add object from dropdown
        item = mask.mask_objects.add()
        item.name = obj_name
        mask_objects[f"MASK{mask_index + 1}"].append(item.name)

        mask.object_dropdown = "NONE"

        return {"FINISHED"}

    # Add all addable selected objects in the scene
    def add_selected_objects(mask, mask_index, selected_objects) -> False:
        addable_object = []

        for obj in selected_objects:
            if obj.type == "MESH" or obj.type == "FONT":
                # The currently selected item is not part of any list
                if not any(item.name == obj.name for item in mask.mask_objects):
                    addable_object.append(obj.name)

        if not addable_object:
            return False

        for addable in addable_object:
            added = mask.mask_objects.add()
            added.name = addable.name
            mask_objects[f"MASK{mask_index + 1}"].append(added.name)

        return True

    # Add all available objects in the scene
    def add_all_objects(self, mask, mask_index):
        for obj in visible_objects:
            if not any(item.name == obj.name for item in mask.mask_objects):
                added = mask.mask_objects.add()
                added.name = obj.name
                mask_objects[f"MASK{mask_index + 1}"].append(added.name)


# Remove the currently selected index in the list from the
# currently selected mask
class MaskObjectListRemoveItem(Operator):
    bl_idname = "list.remove_mask_object_item"
    bl_label = ""
    bl_description = "Remove object"

    @classmethod
    def poll(cls, context):
        mask_index = context.scene.mask_list_index
        mask_props = getattr(context.scene, f"mask_properties{mask_index + 1}")
        return mask_props.mask_objects

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
    bl_description = "Clear objects"

    @classmethod
    def poll(cls, context):
        mask_index = context.scene.mask_list_index
        mask_props = getattr(context.scene, f"mask_properties{mask_index + 1}")
        return mask_props.mask_objects

    def execute(self, context):
        mask_index = context.scene.mask_list_index
        mask = getattr(context.scene, f"mask_properties{mask_index + 1}")

        mask.mask_objects.clear()
        mask_objects[f"MASK{mask_index + 1}"].clear()

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