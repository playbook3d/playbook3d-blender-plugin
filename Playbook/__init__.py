bl_info = {
    "name": "Playbook",
    "description": "Playbook is a generative media platform for teams & studios.",
    "author": "Playbook",
    "location": "Properties > Render > Playbook",
    "version": (1, 1, 1),
    "blender": (4, 2, 0),
    "category": "Render",
}

import bpy


def reset_addon_values():
    from .render_status import RenderStatus

    RenderStatus.is_rendering = False


reset_addon_values()

import os
import toml
from bpy.types import AddonPreferences
from bpy.props import StringProperty
from bpy.app.handlers import persistent
from . import ui
from . import properties
from . import operators
from . import preferences
from .version_control import PlaybookVersionControl
from .utilities.secret_manager import BlenderSecretsManager
from .utilities.network_utilities import get_user_info
from .properties.user_properties import update_user_properties
from . import task_queue


class Preferences(AddonPreferences):
    bl_idname = __package__

    def on_api_key_updated(self, context):
        if not self.api_key:
            return

        if len(self.api_key) != 36:
            return

        user_info = get_user_info()

        if user_info is not None:
            update_user_properties(
                user_info["email"], user_info["teams"], user_info["workflows"]
            )

    api_key: StringProperty(
        name="API Key",
        default="",
        description="Your Playbook API key",
        update=lambda self, context: self.on_api_key_updated(context),
        options={"TEXTEDIT_UPDATE"},
    )

    def draw(self, context):
        layout = self.layout

        if PlaybookVersionControl.can_update:
            layout.alert = True
            layout.label(text=PlaybookVersionControl.version_control_label)
            layout.alert = False
            layout.operator("op.update_addon")
        else:
            layout.label(text=PlaybookVersionControl.version_control_label)

        layout.operator("op.documentation")
        # layout.operator("op.reset_addon_settings")
        layout.prop(self, "api_key")


@persistent
def read_preferences_on_load(dummy):
    addon_prefs = bpy.context.preferences.addons[__package__].preferences

    if not addon_prefs.api_key:
        return

    if len(addon_prefs.api_key) != 36:
        return

    user_info = get_user_info()

    if user_info is not None:
        update_user_properties(
            user_info["email"], user_info["teams"], user_info["workflows"]
        )


def register():
    properties.register()
    ui.register()
    operators.register()
    preferences.register()
    task_queue.register()

    bpy.utils.register_class(Preferences)

    BlenderSecretsManager.load_to_env()

    toml_path = os.path.join(os.path.dirname(__file__), "blender_manifest.toml")
    with open(toml_path, "r") as blender_info:
        version = toml.load(blender_info)["version"]
        PlaybookVersionControl.check_if_version_up_to_date(
            tuple(map(int, version.split(".")))
        )

    if read_preferences_on_load not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(read_preferences_on_load)


def unregister():
    if read_preferences_on_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(read_preferences_on_load)

    try:
        properties.unregister()
        ui.unregister()
        operators.unregister()
        preferences.unregister()
        task_queue.unregister()

        bpy.utils.unregister_class(Preferences)

        reset_addon_values()

    except Exception as e:
        print(e)
        print(e.__traceback__)
