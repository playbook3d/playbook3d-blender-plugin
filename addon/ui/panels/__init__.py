from bpy.utils import register_class, unregister_class
from bpy.props import BoolProperty
from bpy.types import Scene
from .main_panels import MainPanel, CredentialsPanel
from .settings_panels import RenderSettingsPanel, AdvancedSettingsPanel
from .render_panels import RenderPanel
from .misc_panels import ModificationPanel, LinksPanel

classes = [
    MainPanel,
    CredentialsPanel,
    ModificationPanel,
    RenderSettingsPanel,
    AdvancedSettingsPanel,
    RenderPanel,
    LinksPanel,
]


def register():
    global classes
    for cls in classes:
        register_class(cls)

    Scene.show_retexture_panel = BoolProperty(default=True)
    Scene.show_style_panel = BoolProperty(default=False)
    Scene.show_relight_panel = BoolProperty(default=False)
    Scene.is_relight_image = BoolProperty(default=True)
    Scene.show_upscale_panel = BoolProperty(default=False)


def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)

    del Scene.show_retexture_panel
    del Scene.show_style_panel
    del Scene.show_relight_panel
    del Scene.is_relight_image
    del Scene.show_upscale_panel
