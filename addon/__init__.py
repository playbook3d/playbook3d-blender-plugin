bl_info = {
    "name": "Playbook: Render Image",
    "description": "Render the image as seen from the active camera to the Playbook API",
    "author": "Playbook",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "category": "Render",
}

import bpy
from .operators import *
from .panels import *
from .properties import *

NUM_MASK_LAYER = 7

classes = [
    MainPanel,
    GlobalPanel,
    ObjectPanel,
    GlobalProperties,
    MaskProperties1,
    MaskProperties2,
    MaskProperties3,
    MaskProperties4,
    MaskProperties5,
    MaskProperties6,
    MaskProperties7,
    RenderOperator,
]

# Create a mask panel for each mask layer
for i in range(NUM_MASK_LAYER):
    mask_panel = create_mask_panel(i)
    classes.append(mask_panel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.utils.register_class(RenderPanel)

    bpy.types.Scene.global_properties = bpy.props.PointerProperty(type=GlobalProperties)
    # TODO: Is there an alternative to adding each mask property one by one?
    bpy.types.Scene.mask_properties1 = bpy.props.PointerProperty(type=MaskProperties1)
    bpy.types.Scene.mask_properties2 = bpy.props.PointerProperty(type=MaskProperties2)
    bpy.types.Scene.mask_properties3 = bpy.props.PointerProperty(type=MaskProperties3)
    bpy.types.Scene.mask_properties4 = bpy.props.PointerProperty(type=MaskProperties4)
    bpy.types.Scene.mask_properties5 = bpy.props.PointerProperty(type=MaskProperties5)
    bpy.types.Scene.mask_properties6 = bpy.props.PointerProperty(type=MaskProperties6)
    bpy.types.Scene.mask_properties7 = bpy.props.PointerProperty(type=MaskProperties7)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.utils.unregister_class(RenderPanel)

    del bpy.types.Scene.global_properties
    del bpy.types.Scene.mask_properties1
    del bpy.types.Scene.mask_properties2
    del bpy.types.Scene.mask_properties3
    del bpy.types.Scene.mask_properties4
    del bpy.types.Scene.mask_properties5
    del bpy.types.Scene.mask_properties6
    del bpy.types.Scene.mask_properties7


if __name__ == "__main__":
    register()
