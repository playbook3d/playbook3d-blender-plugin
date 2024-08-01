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
import os
from bpy.props import PointerProperty, BoolProperty
from bpy.utils import previews
from .operators import *
from . import ui
from .properties import *
from .utilities import icons as util_icons

NUM_MASK_LAYER = 7

classes = [
    # Operators
    MaskListAddItem,
    MaskListRemoveItem,
    MaskObjectListAddItem,
    MaskObjectListRemoveItem,
    MaskObjectListClearItems,
    LoginOperator,
    UpgradeOperator,
    RetexturePanelOperator,
    RandomizePromptOperator,
    ObjectMaskPanelOperator,
    StylePanelOperator,
    RelightPanelOperator,
    UpscalePanelOperator,
    QueueOperator,
    RenderOperator,
    PlaybookWebsiteOperator,
    PlaybookDiscordOperator,
    PlaybookTwitterOperator,
    ClearStyleImageOperator,
    ClearRelightImageOperator,
]


def register():
    # Custom icons
    icons = previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "images")
    icons.load("playbook_logo", os.path.join(icons_dir, "playbook_logo.png"), "IMAGE")
    icons.load("discord_logo", os.path.join(icons_dir, "discord_logo.png"), "IMAGE")
    icons.load("twitter_logo", os.path.join(icons_dir, "twitter_logo.png"), "IMAGE")
    icons.load("check_icon", os.path.join(icons_dir, "check_icon.png"), "IMAGE")
    icons.load("credit_icon", os.path.join(icons_dir, "credit_icon.png"), "IMAGE")
    util_icons["main"] = icons

    ui.register()

    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)

    properties.register()

    # Set scene properties
    scene = bpy.types.Scene
    scene.general_properties = PointerProperty(type=GeneralProperties)
    scene.style_properties = PointerProperty(type=StyleProperties)
    scene.relight_properties = PointerProperty(type=RelightProperties)
    scene.upscale_properties = PointerProperty(type=UpscaleProperties)
    scene.flag_properties = PointerProperty(type=FlagProperties)

    scene.show_retexture_panel = BoolProperty(default=False)
    scene.show_mask_panel = BoolProperty(default=False)
    scene.show_style_panel = BoolProperty(default=False)
    scene.show_relight_panel = BoolProperty(default=False)
    scene.is_relight_image = BoolProperty(default=True)
    scene.show_upscale_panel = BoolProperty(default=False)

    for i in range(1, 8):
        setattr(
            scene,
            f"mask_properties{i}",
            PointerProperty(type=MaskProperties),
        )


def unregister():
    ui.unregister()

    # Unregister classes
    for cls in classes:
        bpy.utils.unregister_class(cls)

    properties.unregister()

    scene = bpy.types.Scene
    del scene.general_properties
    del scene.style_properties
    del scene.relight_properties
    del scene.upscale_properties
    del scene.flag_properties

    del scene.show_retexture_panel
    del scene.show_mask_panel
    del scene.show_style_panel
    del scene.show_relight_panel
    del scene.is_relight_image
    del scene.show_upscale_panel

    for i in range(1, 8):
        delattr(scene, f"mask_properties{i}")

    # Clear custom icons
    for icon in util_icons.values():
        previews.remove(icon)
    util_icons.clear()
