# pylint: disable=fixme, import-error
import bpy
from bpy.props import (
    PointerProperty,
    IntProperty,
    StringProperty,
    FloatProperty,
    EnumProperty,
    CollectionProperty,
    FloatVectorProperty,
    BoolProperty,
)
from bpy.types import Scene, PropertyGroup
from bpy.utils import register_class, unregister_class
from .ui.lists import MaskObjectListItem
from .objects import visible_objects

NUM_MASKS_ALLOWED = 7


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
            print(obj)
            visible_objects.append(obj)


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
    # Including a "None" option, return a list of the visible objects in the scene
    def update_enum_items(self, context):
        set_visible_objects(context)
        items = [(obj.name, obj.name, "") for obj in visible_objects]
        items.insert(0, ("NONE", "Select an object from the scene", ""))
        items.insert(1, ("BACKGROUND", "Background", ""))

        return items

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
    relight_strength: FloatProperty(name="", default=50, min=0, max=100)


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


classes = [
    GeneralProperties,
    MaskProperties,
    StyleProperties,
    RelightProperties,
    UpscaleProperties,
    FlagProperties,
]


def register():
    global classes
    for cls in classes:
        register_class(cls)

    Scene.general_properties = PointerProperty(type=GeneralProperties)
    Scene.style_properties = PointerProperty(type=StyleProperties)
    Scene.relight_properties = PointerProperty(type=RelightProperties)
    Scene.upscale_properties = PointerProperty(type=UpscaleProperties)
    Scene.flag_properties = PointerProperty(type=FlagProperties)

    for i in range(NUM_MASKS_ALLOWED):
        setattr(
            Scene,
            f"mask_properties{i + 1}",
            PointerProperty(type=MaskProperties),
        )


def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)

    del Scene.general_properties
    del Scene.style_properties
    del Scene.relight_properties
    del Scene.upscale_properties
    del Scene.flag_properties

    for i in range(NUM_MASKS_ALLOWED):
        delattr(Scene, f"mask_properties{i + 1}")
