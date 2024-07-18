import bpy
from bpy.props import StringProperty, FloatProperty, EnumProperty, CollectionProperty
from .visible_objects import visible_objects


# Get all visible mesh objects in the scene
def set_visible_objects():
    visible_objects.clear()
    for obj in bpy.data.objects:
        if obj.visible_get() and obj.type == "MESH":
            visible_objects.append(obj)


# Including a "None" option, return a list of the visible objects in the scene
def update_enum_items(self, context):
    set_visible_objects()
    items = [(obj.name, obj.name, "") for obj in visible_objects]
    items.insert(0, ("None", "None", ""))
    return items


class ObjectProperties(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()


class MaskProperties(bpy.types.PropertyGroup):
    mask_prompt: bpy.props.StringProperty(name="", default="Default value")
    mask_structure_strength: bpy.props.FloatProperty(
        name="", default=50, min=0, max=100
    )
    object_list: bpy.props.CollectionProperty(type=ObjectProperties)
    object_dropdown: bpy.props.EnumProperty(
        name="",
        items=update_enum_items,
        update=lambda self, context: self.update_enum(context),
    )

    def is_value_in_list(self, value):
        for item in self.object_list:
            if item.value == value:
                return True
        return False

    # Add the selected dropdown option to the mask object list
    def update_enum(self, context):
        # Ignore if value is already in list
        if self.is_value_in_list(self.object_dropdown):
            return

        # Ignore if value is none
        if self.object_dropdown == "None":
            return

        new_item = self.object_list.add()
        new_item.name = self.object_dropdown
        print(new_item.name)


class RenderProperties(bpy.types.PropertyGroup):
    global_prompt: bpy.props.StringProperty(name="", default="Default value")
    global_structure_strength: bpy.props.FloatProperty(
        name="", default=50, min=0, max=100
    )
