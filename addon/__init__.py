bl_info = {
    "name": "Playbook: Render Image",
    "description": "Render the image as seen from the active camera to the Playbook API",
    "author": "Playbook",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "category": "Render",
}

import bpy
from .operators import RenderOperator
from .panels import *
from .properties import *

NUM_MASK_LAYER = 7

classes = [
    RenderOperator,
    MainPanel,
    ObjectProperties,
    MaskProperties,
    RenderProperties,
]

# Create a mask panel for each mask layer
for i in range(NUM_MASK_LAYER):
    mask_panel = create_mask_panel(i)
    classes.append(mask_panel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.utils.register_class(RenderPanel)

    # TODO: Is there an alternative to adding each mask property one by one?
    bpy.types.Scene.object_properties = bpy.props.PointerProperty(type=ObjectProperties)
    bpy.types.Scene.mask_properties1 = bpy.props.PointerProperty(type=MaskProperties)
    bpy.types.Scene.mask_properties2 = bpy.props.PointerProperty(type=MaskProperties)
    bpy.types.Scene.mask_properties3 = bpy.props.PointerProperty(type=MaskProperties)
    bpy.types.Scene.mask_properties4 = bpy.props.PointerProperty(type=MaskProperties)
    bpy.types.Scene.mask_properties5 = bpy.props.PointerProperty(type=MaskProperties)
    bpy.types.Scene.mask_properties6 = bpy.props.PointerProperty(type=MaskProperties)
    bpy.types.Scene.mask_properties7 = bpy.props.PointerProperty(type=MaskProperties)
    bpy.types.Scene.render_properties = bpy.props.PointerProperty(type=RenderProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.utils.unregister_class(RenderPanel)

    del bpy.types.Scene.object_properties
    del bpy.types.Scene.mask_properties1
    del bpy.types.Scene.mask_properties2
    del bpy.types.Scene.mask_properties3
    del bpy.types.Scene.mask_properties4
    del bpy.types.Scene.mask_properties5
    del bpy.types.Scene.mask_properties6
    del bpy.types.Scene.mask_properties7
    del bpy.types.Scene.render_properties


if __name__ == "__main__":
    register()
