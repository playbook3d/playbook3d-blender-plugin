from .panels import *
from .lists import *


def register():
    lists.register()
    panels.register()


def unregister():
    lists.unregister()
    panels.unregister()
