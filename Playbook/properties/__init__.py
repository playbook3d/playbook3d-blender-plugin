from . import workflow_properties
from . import teams_properties


def register():
    workflow_properties.register()
    teams_properties.register()


def unregister():
    workflow_properties.unregister()
    teams_properties.unregister()
