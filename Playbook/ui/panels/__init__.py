from bpy.utils import register_class, unregister_class
from bpy.props import BoolProperty
from bpy.types import Scene
from .main_panels import *
from .teams_panels import *
from .settings_panels import *
from .render_panels import *
from .misc_panels import *
from . import panel_operators

classes = [
    MainPanel3D,
    MainPanelRender,
    CredentialsPanel3D,
    CredentialsPanelRender,
    TeamsPanel3D,
    TeamsPanelRender,
    AdvancedSettingsPanel3D,
    AdvancedSettingsPanelRender,
    RenderPanel3D,
    RenderPanelRender,
    LinksPanel3D,
    LinksPanelRender,
]


def register():
    global classes
    for cls in classes:
        register_class(cls)

    panel_operators.register()

    Scene.show_style_panel = BoolProperty(default=False)
    Scene.show_relight_panel = BoolProperty(default=False)
    Scene.is_relight_image = BoolProperty(default=True)
    Scene.show_upscale_panel = BoolProperty(default=False)


def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)

    panel_operators.unregister()

    del Scene.show_style_panel
    del Scene.show_relight_panel
    del Scene.is_relight_image
    del Scene.show_upscale_panel
