bl_info = {
    "name": "Playbook",
    "description": "Playbook is a diffusion based engine for 3D scenes.",
    "author": "Playbook",
    "location": "Properties > Render > Playbook",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "category": "Render",
    "doc_url": "https://www.playbookengine.com",
}

import bpy
from bpy.props import PointerProperty, BoolProperty
from .operators import *
from .panels import *
from .properties import *

NUM_MASK_LAYER = 7

classes = [
    # Panels
    MainPanel,
    CredentialsPanel,
    GlobalPanel,
    #
    # Properties
    GlobalProperties,
    MaskProperties1,
    MaskProperties2,
    MaskProperties3,
    MaskProperties4,
    MaskProperties5,
    MaskProperties6,
    MaskProperties7,
    #
    # Operators
    LoginOperator,
    CreditsOperator,
    GlobalPanelOperator,
    ObjectMaskPanelOperator,
    QueueOperator,
    RenderOperator,
    PlaybookWebsiteOperator,
    PlaybookDiscordOperator,
]

# Create a mask panel for each mask layer
# for i in range(NUM_MASK_LAYER):
#     mask_panel = create_mask_panel(i)
#     classes.append(mask_panel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.utils.register_class(RenderPanel)
    bpy.utils.register_class(LinksPanel)

    scene = bpy.types.Scene
    scene.global_properties = PointerProperty(type=GlobalProperties)
    scene.show_global_panel = BoolProperty(default=False)
    scene.show_mask_panel = BoolProperty(default=False)

    for i in range(1, 8):
        setattr(
            scene,
            f"mask_properties{i}",
            PointerProperty(type=eval(f"MaskProperties{i}")),
        )
        setattr(scene, f"show_mask_properties{i}", BoolProperty(default=False))


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.utils.unregister_class(RenderPanel)
    bpy.utils.unregister_class(LinksPanel)

    scene = bpy.types.Scene
    del scene.global_properties
    del scene.show_global_panel
    del scene.show_mask_panel

    for i in range(1, 8):
        delattr(scene, f"mask_properties{i}")
        delattr(scene, f"show_mask_properties{i}")
