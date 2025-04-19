import bpy
from bpy.utils import register_class, unregister_class
from bpy.types import Operator
from ...objects.visible_objects import visible_objects, allowed_obj_types
from ...objects.objects import mask_objects

MAX_MASKS = 3


def is_object_part_of_a_mask(obj_name: str):
    return any(obj_name in obj_list for obj_list in mask_objects.values())


class MaskListAddItem(Operator):
    bl_idname = "list.add_mask_item"
    bl_label = ""
    bl_description = "Add mask"

    @classmethod
    def poll(cls, context):
        return len(context.scene.mask_list) < 7

    def execute(self, context):
        mask_len = len(context.scene.mask_list)
        if mask_len == MAX_MASKS:
            return {"CANCELLED"}

        item = context.scene.mask_list.add()
        item.name = f"Mask {mask_len + 1}"
        context.scene.mask_list_index = len(context.scene.mask_list) - 1
        return {"FINISHED"}


class MaskListRemoveItem(Operator):
    bl_idname = "list.remove_mask_item"
    bl_label = ""
    bl_description = "Remove mask"

    @classmethod
    def poll(cls, context):
        return len(context.scene.mask_list) > 1

    def execute(self, context):
        scene = context.scene
        mask_list = scene.mask_list
        index = scene.mask_list_index

        if index >= len(mask_list):
            return {"CANCELLED"}

        mask_key = f"MASK{index + 1}"
        fallback_key = "MASK1"
        fallback_index = 0  # MASK8 is the 8th slot
        fallback_props = getattr(scene, f"mask_properties{fallback_index + 1}")

        if fallback_key not in mask_objects:
            mask_objects[fallback_key] = []

        # Move all objects from the deleted mask into MASK8
        for obj_name in mask_objects.get(mask_key, []):
            # Remove from all masks just in case of bad state
            for key, obj_list in mask_objects.items():
                if obj_name in obj_list:
                    obj_list.remove(obj_name)

                    # Also remove from UI collection
                    props = getattr(scene, f"mask_properties{int(key[-1])}")  # parse MASK#
                    for i, item in enumerate(props.mask_objects):
                        if item.name == obj_name:
                            props.mask_objects.remove(i)
                            break

            # Add to fallback if not already there
            if obj_name not in mask_objects[fallback_key]:
                item = fallback_props.mask_objects.add()
                item.name = obj_name
                mask_objects[fallback_key].append(obj_name)

        # Clear the deleted mask data
        mask_objects[mask_key].clear()

        # Remove from UI list
        mask_list.remove(index)
        scene.mask_list_index = 0 if len(mask_list) > 0 else -1

        return {"FINISHED"}


class MaskObjectListAddItem(Operator):
    bl_idname = "list.add_mask_object_item"
    bl_label = ""
    bl_description = "Add object"

    @classmethod
    def poll(cls, context):
        selected_objects = [obj for obj in context.selected_objects]
        if selected_objects:
            for obj in selected_objects:
                if obj.type not in allowed_obj_types:
                    continue
                if is_object_part_of_a_mask(obj.name):
                    continue
                return True
            return False

        mask_index = context.scene.mask_list_index
        mask = getattr(context.scene, f"mask_properties{mask_index + 1}")
        return mask.object_dropdown != "NONE"

    def execute(self, context):
        mask_index = context.scene.mask_list_index
        mask = getattr(context.scene, f"mask_properties{mask_index + 1}")

        selected_objects = [obj for obj in context.selected_objects]
        if selected_objects:
            if self.add_selected_objects(mask, mask_index, selected_objects):
                return {"FINISHED"}

        if mask.object_dropdown == "NONE":
            return {"CANCELLED"}
        elif mask.object_dropdown == "ADDALL":
            self.add_all_objects(mask, mask_index)
            mask.object_dropdown = "NONE"
            return {"FINISHED"}
        elif mask.object_dropdown == "BACKGROUND":
            obj_name = "Background"
        else:
            obj_name = mask.object_dropdown

        item = mask.mask_objects.add()
        item.name = obj_name
        mask_objects[f"MASK{mask_index + 1}"].append(item.name)
        mask.object_dropdown = "NONE"
        return {"FINISHED"}

    def add_selected_objects(self, mask, mask_index, selected_objects) -> bool:
        addable_object = []
        for obj in selected_objects:
            if obj.type in allowed_obj_types and not is_object_part_of_a_mask(obj.name):
                addable_object.append(obj.name)

        if not addable_object:
            return False

        for addable in addable_object:
            added = mask.mask_objects.add()
            added.name = addable
            mask_objects[f"MASK{mask_index + 1}"].append(addable)
        return True

    def add_all_objects(self, mask, mask_index):
        for obj in visible_objects:
            if not is_object_part_of_a_mask(obj.name):
                added = mask.mask_objects.add()
                added.name = obj.name
                mask_objects[f"MASK{mask_index + 1}"].append(added.name)


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
            else len(mask.mask_objects) - 1
        )

        mask.mask_objects.remove(index)
        mask_objects[f"MASK{mask_index + 1}"].pop(index)
        mask.object_list_index = 0 if mask.mask_objects else -1
        return {"FINISHED"}


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
