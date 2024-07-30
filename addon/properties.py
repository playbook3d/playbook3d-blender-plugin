# pylint: disable=fixme, import-error
import bpy
from bpy.props import (
    IntProperty,
    StringProperty,
    FloatProperty,
    EnumProperty,
    CollectionProperty,
    FloatVectorProperty,
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
    ("PHOTOREAL", "Photoreal", ""),
    ("ANIME", "Anime", ""),
    ("3DCARTOON", "3D Cartoon", ""),
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
    items.insert(0, ("None", "None", ""))
    items.insert(1, ("Background", "Background", ""))

    return items


# Properties of each item in the mask list
class MaskListItem(PropertyGroup):
    mask_name: StringProperty(name="")


# Properties of each item in the mask objects list
class MaskObjectListItem(PropertyGroup):
    object_name: StringProperty(name="")
    object_id: StringProperty(name="")


# Properties under the 'General' panel
class GeneralProperties(PropertyGroup):
    general_prompt: StringProperty(name="", default="Describe the scene...")
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
    )


# Properties under the 'Style Transfer' panel
class StyleProperties(PropertyGroup):
    style_image: StringProperty(name="", subtype="FILE_PATH", maxlen=1024)
    style_strength: FloatProperty(name="", default=50, min=0, max=100)


# Properties under the 'Relight' panel
class RelightProperties(PropertyGroup):
    def update_type(self, context):
        context.scene.is_relight_image = self.relight_type == "IMAGE"

    relight_type: EnumProperty(
        name="Type",
        items=[("IMAGE", "Image", ""), ("COLOR", "Color", "")],
        update=lambda self, context: self.update_type(context),
    )
    relight_image: StringProperty(name="", subtype="FILE_PATH", maxlen=1024)
    relight_color: FloatVectorProperty(
        name="", subtype="COLOR", default=(1, 1, 1, 1), size=4
    )
    relight_strength: FloatProperty(name="", default=0, min=0, max=100)


# Properties under the 'Upscale' panel
class UpscaleProperties(PropertyGroup):
    upscale_scale: EnumProperty(name="", items=upscale_options)
