import bpy
from . import lists
from . import list_operators


def register():
    lists.register()
    list_operators.register()


def unregister():
    lists.unregister()
    list_operators.unregister()
