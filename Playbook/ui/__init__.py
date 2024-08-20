import bpy
from . import lists
from . import list_operators
from . import panels
from . import panel_operators
from . import icons


def register():
    lists.register()
    list_operators.register()
    panels.register()
    panel_operators.register()
    icons.register()


def unregister():
    lists.unregister()
    list_operators.unregister()
    panels.unregister()
    panel_operators.unregister()
    icons.unregister
