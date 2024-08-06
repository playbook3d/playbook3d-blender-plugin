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

from . import ui
from .properties import *
from .operators import *
from bpy.app.handlers import persistent


def register():
    ui.register()
    properties.register()
    operators.register()


def unregister():
    ui.unregister()
    properties.unregister()
    operators.unregister()
