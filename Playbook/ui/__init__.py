from . import panels
from . import icons


def register():
    panels.register()
    icons.register()


def unregister():
    panels.unregister()
    icons.unregister()
