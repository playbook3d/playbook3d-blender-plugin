# pylint: disable=fixme, import-error
import bpy
from bpy.props import StringProperty, FloatProperty, EnumProperty


visible_objects = []

mask_objects = {
    "MASK1": "",
    "MASK2": "",
    "MASK3": "",
    "MASK4": "",
    "MASK5": "",
    "MASK6": "",
    "MASK7": "",
}

prompt_styles = [
    ("PHOTOREAL", "Photoreal", ""),
    ("ANIME", "Anime", ""),
    ("3DCARTOON", "3D Cartoon", ""),
]


# Get all visible mesh objects in the scene
def set_visible_objects(context):
    visible_objects.clear()
    for obj in context.scene.objects:
        if obj.type == "MESH" and obj.visible_get():
            visible_objects.append(obj)


# Including a "None" option, return a list of the visible objects in the scene
def update_enum_items(self, context):
    set_visible_objects(context)
    items = [(obj.name, obj.name, "") for obj in visible_objects]
    items.insert(0, ("None", "None", ""))
    items.insert(1, ("Background", "Background", ""))

    return items


class GlobalProperties(bpy.types.PropertyGroup):
    global_prompt: StringProperty(name="", default="Describe the scene...")
    global_structure_strength: FloatProperty(name="", default=50, min=0, max=100)
    global_style: EnumProperty(
        name="",
        items=prompt_styles,
        options={"ANIMATABLE"},
    )


class MaskProperties1(bpy.types.PropertyGroup):
    # Add the selected dropdown option to the mask object list
    def update_enum(self, context):
        mask_objects["MASK1"] = self.object_dropdown

    mask_prompt: StringProperty(name="", default="Describe the scene...")
    mask_isolate: FloatProperty(name="", default=50, min=0, max=100)
    mask_style: EnumProperty(
        name="",
        items=prompt_styles,
        options={"ANIMATABLE"},
    )
    object_dropdown: EnumProperty(
        name="",
        items=update_enum_items,
        update=lambda self, context: self.update_enum(context),
    )


class MaskProperties2(bpy.types.PropertyGroup):
    # Add the selected dropdown option to the mask object list
    def update_enum(self, context):
        mask_objects["MASK2"] = self.object_dropdown

    mask_prompt: StringProperty(name="", default="Describe the scene...")
    mask_isolate: FloatProperty(name="", default=50, min=0, max=100)
    mask_style: EnumProperty(
        name="",
        items=prompt_styles,
        options={"ANIMATABLE"},
    )
    object_dropdown: EnumProperty(
        name="",
        items=update_enum_items,
        update=lambda self, context: self.update_enum(context),
    )


class MaskProperties3(bpy.types.PropertyGroup):
    # Add the selected dropdown option to the mask object list
    def update_enum(self, context):
        mask_objects["MASK3"] = self.object_dropdown

    mask_prompt: StringProperty(name="", default="Describe the scene...")
    mask_isolate: FloatProperty(name="", default=50, min=0, max=100)
    mask_style: EnumProperty(
        name="",
        items=prompt_styles,
        options={"ANIMATABLE"},
    )
    object_dropdown: EnumProperty(
        name="",
        items=update_enum_items,
        update=lambda self, context: self.update_enum(context),
    )


class MaskProperties4(bpy.types.PropertyGroup):
    # Add the selected dropdown option to the mask object list
    def update_enum(self, context):
        mask_objects["MASK4"] = self.object_dropdown

    mask_prompt: StringProperty(name="", default="Describe the scene...")
    mask_isolate: FloatProperty(name="", default=50, min=0, max=100)
    mask_style: EnumProperty(
        name="",
        items=prompt_styles,
        options={"ANIMATABLE"},
    )
    object_dropdown: EnumProperty(
        name="",
        items=update_enum_items,
        update=lambda self, context: self.update_enum(context),
    )


class MaskProperties5(bpy.types.PropertyGroup):
    # Add the selected dropdown option to the mask object list
    def update_enum(self, context):
        mask_objects["MASK5"] = self.object_dropdown

    mask_prompt: StringProperty(name="", default="Describe the scene...")
    mask_isolate: FloatProperty(name="", default=50, min=0, max=100)
    mask_style: EnumProperty(
        name="",
        items=prompt_styles,
        options={"ANIMATABLE"},
    )
    object_dropdown: EnumProperty(
        name="",
        items=update_enum_items,
        update=lambda self, context: self.update_enum(context),
    )


class MaskProperties6(bpy.types.PropertyGroup):
    # Add the selected dropdown option to the mask object list
    def update_enum(self, context):
        mask_objects["MASK6"] = self.object_dropdown

    mask_prompt: StringProperty(name="", default="Describe the scene...")
    mask_isolate: FloatProperty(name="", default=50, min=0, max=100)
    mask_style: EnumProperty(
        name="",
        items=prompt_styles,
        options={"ANIMATABLE"},
    )
    object_dropdown: EnumProperty(
        name="",
        items=update_enum_items,
        update=lambda self, context: self.update_enum(context),
    )


class MaskProperties7(bpy.types.PropertyGroup):

    # Add the selected dropdown option to the mask object list
    def update_enum(self, context):
        mask_objects["MASK7"] = self.object_dropdown

    mask_prompt: StringProperty(name="", default="Describe the scene...")
    mask_isolate: FloatProperty(name="", default=50, min=0, max=100)
    mask_style: EnumProperty(
        name="",
        items=prompt_styles,
        options={"ANIMATABLE"},
    )
    object_dropdown: EnumProperty(
        name="",
        items=update_enum_items,
        update=lambda self, context: self.update_enum(context),
    )
