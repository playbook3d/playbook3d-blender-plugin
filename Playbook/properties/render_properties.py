import bpy
from bpy.props import PointerProperty, IntProperty, EnumProperty
from bpy.types import Scene, PropertyGroup
from bpy.utils import register_class, unregister_class


#
class RenderProperties(PropertyGroup):
    def get_masks(self, context):
        scene = context.scene

        if hasattr(scene, "mask_list"):
            mask_list = scene.mask_list

            dropdown_options = [
                (mask.name.upper(), mask.name, mask.name) for mask in mask_list
            ]
            dropdown_options.insert(0, ("NONE", "None", "None"))
        else:
            dropdown_options = [("NONE", "None", "None")]

        return dropdown_options

    def on_update_preserve_mask(self, context):
        dropdown_item = self.preserve_mask_dropdown
        items = self.get_masks(context)

        index = next(
            (i for i, item in enumerate(items) if item[0] == dropdown_item), None
        )
        self.preserve_mask_index = index

    preserve_mask_index: IntProperty(
        name="",
    )
    preserve_mask_dropdown: EnumProperty(
        name="",
        items=get_masks,
        update=lambda self, context: self.on_update_preserve_mask(context),
    )


def register():
    register_class(RenderProperties)

    Scene.render_properties = PointerProperty(type=RenderProperties)


def unregister():
    unregister_class(RenderProperties)

    del Scene.render_properties
