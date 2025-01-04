from bpy.props import StringProperty, BoolProperty
from bpy.types import Scene
from . import mask_properties
from . import user_properties
from . import render_properties
from . import lists


def register():
    lists.register()
    user_properties.register()
    mask_properties.register()
    render_properties.register()

    Scene.error_message = StringProperty(default="")
    Scene.status_message = StringProperty(default="")
    Scene.show_object_dropdown = BoolProperty(default=False)


def unregister():
    lists.unregister()
    user_properties.unregister()
    mask_properties.unregister()
    render_properties.unregister()

    del Scene.error_message
    del Scene.status_message
    del Scene.show_object_dropdown
