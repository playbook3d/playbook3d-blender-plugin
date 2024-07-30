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
from bpy.props import PointerProperty, IntProperty, BoolProperty, CollectionProperty
from bpy.utils import previews
from .operators import *
from .panels import *
from .properties import *
from .utilities import icons as util_icons, PB_UL_CustomList

NUM_MASK_LAYER = 7

classes = [
    #
    # Panels
    MainPanel,
    CredentialsPanel,
    RenderSettingsPanel,
    RenderPanel,
    LinksPanel,
    #
    # Properties
    MaskListItem,
    MaskListAddItem,
    MaskListRemoveItem,
    MaskObjectListItem,
    MaskObjectListAddItem,
    MaskObjectListRemoveItem,
    MaskObjectListClearItems,
    GeneralProperties,
    MaskProperties,
    StyleProperties,
    RelightProperties,
    UpscaleProperties,
    #
    # Operators
    LoginOperator,
    UpgradeOperator,
    RetexturePanelOperator,
    RandomizePromptOperator,
    ObjectMaskPanelOperator,
    MaskPropertyPanelOperator1,
    MaskPropertyPanelOperator2,
    MaskPropertyPanelOperator3,
    MaskPropertyPanelOperator4,
    MaskPropertyPanelOperator5,
    MaskPropertyPanelOperator6,
    MaskPropertyPanelOperator7,
    StylePanelOperator,
    RelightPanelOperator,
    UpscalePanelOperator,
    QueueOperator,
    RenderOperator,
    PlaybookWebsiteOperator,
    PlaybookDiscordOperator,
    PlaybookTwitterOperator,
    #
    # UI
    PB_UL_CustomList,
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

    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)

    # Set scene properties
    scene = bpy.types.Scene
    scene.general_properties = PointerProperty(type=GeneralProperties)
    scene.style_properties = PointerProperty(type=StyleProperties)
    scene.relight_properties = PointerProperty(type=RelightProperties)
    scene.upscale_properties = PointerProperty(type=UpscaleProperties)

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

    scene.mask_list = CollectionProperty(type=MaskListItem)
    scene.mask_list_index = IntProperty(name="", default=-1)


def unregister():
    # Unregister classes
    for cls in classes:
        bpy.utils.unregister_class(cls)

    scene = bpy.types.Scene
    del scene.general_properties
    del scene.style_properties
    del scene.relight_properties
    del scene.upscale_properties

    del scene.show_retexture_panel
    del scene.show_mask_panel
    del scene.show_style_panel
    del scene.show_relight_panel
    del scene.is_relight_image
    del scene.show_upscale_panel

    for i in range(1, 8):
        delattr(scene, f"mask_properties{i}")

    del scene.mask_list
    del scene.mask_list_index

    # Clear custom icons
    for icon in util_icons.values():
        previews.remove(icon)
    util_icons.clear()
