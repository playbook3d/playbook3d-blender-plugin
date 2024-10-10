bl_info = {
    "name": "Playbook",
    "description": "Playbook is a diffusion based engine for 3D scenes. Press 'N' to bring up the plugin window.",
    "author": "Playbook",
    "location": "Properties > Render > Playbook",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "category": "Render",
}

import sys
import subprocess
import os


def install_packages():
    addon_dir = os.path.dirname(__file__)
    requirements_path = os.path.join(addon_dir, "requirements.txt")

    python_executable = sys.executable
    try:
        with open(requirements_path, "r") as f:
            packages = f.readlines()
        for package in packages:
            package_name = package.split("==")[0]
            try:
                __import__(package_name)
            except ImportError:
                subprocess.check_call(
                    [python_executable, "-m", "pip", "install", package]
                )
    except Exception as e:
        print(f"Error reading requirements.txt: {e}")


# Call the install_packages function
install_packages()

import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty
from . import ui
from . import properties
from . import operators
from . import preferences
from . import render_image
from .version_control import UpdateChecker
from .utilities.network_utilities import get_user_info


class Preferences(AddonPreferences):
    bl_idname = __name__

    def on_api_key_updated(self, context):
        if not self.api_key:
            return

        user_info = get_user_info(self.api_key)
        context.scene.user_properties.user_email = user_info["email"]
        context.scene.user_properties.user_credits = user_info["credits"]

    api_key: StringProperty(
        name="API Key",
        default="",
        description="Your Playbook API Key",
        update=lambda self, context: self.on_api_key_updated(context),
    )

    def draw(self, context):
        layout = self.layout

        if UpdateChecker.can_update:
            layout.alert = True
            layout.label(text="You can update to our latest version.")
            layout.alert = False
            layout.operator("op.update_addon")
        else:
            layout.label(text="You have the latest version of Playbook.")

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

    UpdateChecker.check_if_version_up_to_date(bl_info["version"])


def unregister():
    ui.unregister()
    properties.unregister()
    operators.unregister()
    preferences.unregister()
    render_image.unregister()

    bpy.utils.unregister_class(Preferences)
