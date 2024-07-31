# pylint: disable=fixme, import-error
import bpy
from bpy.props import (
    IntProperty,
    StringProperty,
    FloatProperty,
    EnumProperty,
    CollectionProperty,
    FloatVectorProperty,
    BoolProperty,
)
from bpy.types import PropertyGroup


visible_objects = []

# Objects that are part of each mask
mask_objects = {
    "MASK1": [],
    "MASK2": [],
    "MASK3": [],
    "MASK4": [],
    "MASK5": [],
    "MASK6": [],
    "MASK7": [],
}

# Available general model options
prompt_styles = [
    ("PHOTOREAL1", "Photoreal", ""),
    ("PHOTOREAL2", "Photoreal (humans)", ""),
    ("PHOTOREAL3", "Photoreal (product photography)", ""),
    ("ANIME", "Anime", ""),
    ("3DCARTOON", "3D Cartoon", ""),
]

angle_options = [
    ("TOPLEFT", "Top left", ""),
    ("TOPRIGHT", "Top right", ""),
    ("BOTTOMLEFT", "Bottom left", ""),
    ("BOTTOMRIGHT", "Bottom right", ""),
]

# Available upscale options
upscale_options = [("1", "1x", ""), ("2", "2x", ""), ("4", "4x", "")]


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
    items.insert(0, ("NONE", "None", ""))
    items.insert(1, ("BACKGROUND", "Background", ""))

    return items


# Properties of each item in the mask list
class MaskListItem(PropertyGroup):
    mask_name: StringProperty(name="")


# Properties of each item in the mask objects list
class MaskObjectListItem(PropertyGroup):
    object_name: StringProperty(name="")


# Properties under the 'General' panel
class GeneralProperties(PropertyGroup):
    def on_update_prompt(self, context):
        if not self.general_prompt:
            self.general_prompt = "Describe the scene..."
            context.scene.flag_properties.retexture_flag = False
        else:
            context.scene.flag_properties.retexture_flag = True

    general_prompt: StringProperty(
        name="",
        default="Describe the scene...",
        update=lambda self, context: self.on_update_prompt(context),
    )
    general_structure_strength: FloatProperty(name="", default=50, min=0, max=100)
    general_style: EnumProperty(
        name="",
        items=prompt_styles,
        options={"ANIMATABLE"},
    )


#
class MaskProperties(PropertyGroup):
    mask_objects: CollectionProperty(type=MaskObjectListItem, name="")
    object_list_index: IntProperty(name="", default=-1)
    mask_prompt: StringProperty(name="", default="Describe masked objects...")
    mask_isolate: FloatProperty(name="", default=50, min=0, max=100)
    mask_style: EnumProperty(
        name="",
        items=prompt_styles,
        options={"ANIMATABLE"},
    )
    object_dropdown: EnumProperty(
        name="",
        items=update_enum_items,
    )


# Properties under the 'Style Transfer' panel
class StyleProperties(PropertyGroup):
    def on_update_image(self, context):
        context.scene.flag_properties.style_flag = self.style_image

    style_image: StringProperty(
        name="",
        subtype="FILE_PATH",
        maxlen=1024,
        update=lambda self, context: self.on_update_image(context),
    )
    style_strength: FloatProperty(name="", default=50, min=0, max=100)


# Properties under the 'Relight' panel
class RelightProperties(PropertyGroup):
    def on_update_image(self, context):
        context.scene.flag_properties.relight_flag = self.relight_image

    def on_update_prompt(self, context):
        if not self.relight_prompt:
            self.relight_prompt = "Describe the lighting..."
            context.scene.flag_properties.relight_flag = False
        else:
            context.scene.flag_properties.relight_flag = True

    def on_update_angle(self, context):
        context.scene.flag_properties.relight_flag = self.relight_angle != "TOPLEFT"

    def update_type(self, context):
        context.scene.is_relight_image = self.relight_type == "IMAGE"

    relight_type: EnumProperty(
        name="Type",
        items=[("IMAGE", "Image", ""), ("COLOR", "Color", "")],
        update=lambda self, context: self.update_type(context),
    )
    relight_image: StringProperty(
        name="",
        subtype="FILE_PATH",
        maxlen=1024,
        update=lambda self, context: self.on_update_image(context),
    )
    relight_color: FloatVectorProperty(
        name="", subtype="COLOR", default=(1, 1, 1, 1), size=4
    )
    relight_prompt: StringProperty(
        name="",
        default="Describe the lighting...",
        update=lambda self, context: self.on_update_prompt(context),
    )
    relight_angle: EnumProperty(
        name="",
        items=angle_options,
        update=lambda self, context: self.on_update_angle(context),
    )
    relight_strength: FloatProperty(name="", default=0, min=0, max=100)


# Properties under the 'Upscale' panel
class UpscaleProperties(PropertyGroup):
    def on_update_scale(self, context):
        context.scene.flag_properties.upscale_flag = self.upscale_scale != "1"

    upscale_scale: EnumProperty(
        name="",
        items=upscale_options,
        update=lambda self, context: self.on_update_scale(context),
    )


# Flags to keep track if the properties were modified
class FlagProperties(PropertyGroup):
    retexture_flag: BoolProperty(name="", default=False)
    style_flag: BoolProperty(name="", default=False)
    relight_flag: BoolProperty(name="", default=False)
    upscale_flag: BoolProperty(name="", default=False)
