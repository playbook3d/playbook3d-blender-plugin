bl_info = {
    "name": "Playbook",
    "description": "Playbook is a diffusion based engine for 3D scenes.",
    "author": "Playbook",
    "location": "Properties > Render > Playbook",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "category": "Render",
    "doc_url": "https://www.playbook3d.com",
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
from . import ui
from . import properties
from . import operators


class AddonPreference(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout

        layout.operator("op.reset_addon_settings", text="Reset Addon")


def register():
    ui.register()
    properties.register()
    operators.register()
    bpy.utils.register_class(AddonPreference)


def unregister():
    ui.unregister()
    properties.unregister()
    operators.unregister()
    bpy.utils.unregister_class(AddonPreference)
