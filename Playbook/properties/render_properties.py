import bpy
from bpy.props import PointerProperty, BoolProperty, IntProperty
from bpy.types import Scene, PropertyGroup
from bpy.utils import register_class, unregister_class


#
class RenderProperties(PropertyGroup):
    beauty_pass_checkbox: BoolProperty(name="Beauty Pass", default=True)
    mask_pass_checkbox: BoolProperty(name="Mask Pass", default=False)
    outline_pass_checkbox: BoolProperty(name="Outline Pass", default=False)
    normal_pass_checkbox: BoolProperty(name="Normal Pass", default=False)

    # Sequence Capture
    is_capturing_sequence: BoolProperty(name="", default=False)
    capture_count: IntProperty(name="", default=0)


def register():
    register_class(RenderProperties)

    Scene.render_properties = PointerProperty(type=RenderProperties)


def unregister():
    unregister_class(RenderProperties)

    del Scene.render_properties
