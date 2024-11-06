bl_info = {
    "name": "Playbook",
    "description": "Playbook is a diffusion based renderer for 3D scenes. Press 'N' to bring up the plugin window.",
    "author": "Playbook 3D",
    "location": "Properties > Render > Playbook",
    "version": (1, 0, 3),
    "blender": (4, 0, 0),
    "category": "Render",
}

import bpy


def ensure_packages():
    if bpy.app.version < (4, 2, 0):
        import site
        import sys
        import os
        import subprocess
        import importlib
        import importlib.util

        requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")

        user_sites = site.getusersitepackages()
        os.makedirs(user_sites, exist_ok=True)
        sys.path.append(user_sites)

        python_executable = sys.executable
        try:
            with open(requirements_path, "r") as f:
                packages = [
                    package
                    for package in f.read().splitlines()
                    if not importlib.util.find_spec(package)
                ]
                subprocess.run([python_executable, "-m", "ensurepip", "--upgrade"])
                subprocess.run(
                    [python_executable, "-m", "pip", "install", *packages, "--user"],
                    check=True,
                )

        except Exception as e:
            print(f"Error reading requirements.txt: {e}")

    import dotenv

    print(dotenv.__file__)


def reset_addon_values():
    from .render_status import RenderStatus

    RenderStatus.is_rendering = False


ensure_packages()
reset_addon_values()

import os
import toml
from bpy.types import AddonPreferences
from bpy.props import StringProperty
from . import ui
from . import properties
from . import operators
from . import preferences
from . import render_image
from .version_control import PlaybookVersionControl
from .utilities.secret_manager import BlenderSecretsManager
from .utilities.network_utilities import get_user_info


class Preferences(AddonPreferences):
    bl_idname = __package__

    def on_api_key_updated(self, context):
        if not self.api_key:
            return

        if len(self.api_key) != 36:
            return

        user_info = get_user_info(self.api_key)

        if user_info is not None:
            context.scene.user_properties.user_email = user_info["email"]
            context.scene.user_properties.user_credits = user_info["credits"]

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
        layout.operator("op.reset_addon_settings")
        layout.prop(self, "api_key")


def register():
    ui.register()
    properties.register()
    operators.register()
    preferences.register()
    render_image.register()

    bpy.utils.register_class(Preferences)
    BlenderSecretsManager.load_to_env()
    toml_path = os.path.join(os.path.dirname(__file__), "blender_manifest.toml")
    with open(toml_path, "r") as blender_info:
        version = toml.load(blender_info)["version"]
        PlaybookVersionControl.check_if_version_up_to_date(
            tuple(map(int, version.split(".")))
        )


def unregister():
    try:
        ui.unregister()
        properties.unregister()
        operators.unregister()
        preferences.unregister()
        render_image.unregister()

        bpy.utils.unregister_class(Preferences)

        reset_addon_values()

    except Exception as e:
        print(e)
        print(e.__traceback__)
