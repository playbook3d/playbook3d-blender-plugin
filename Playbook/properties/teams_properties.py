import bpy
from bpy.props import EnumProperty, PointerProperty
from bpy.types import PropertyGroup, Scene
from bpy.utils import register_class, unregister_class

temp_teams = [("REDBULL", "Red Bull", "")]
temp_projects = [("REDBULLAD", "Red Bull Ad", "")]


#
class TeamsProperties(PropertyGroup):
    def on_update_team(self, context):
        print(self.teams_dropdown)

    def on_update_project(self, context):
        print(self.projects_dropdown)

    teams_dropdown: EnumProperty(
        name="",
        items=temp_teams,
        update=lambda self, context: self.on_update_team(context),
    )
    projects_dropdown: EnumProperty(
        name="",
        items=temp_projects,
        update=lambda self, context: self.on_update_project(context),
    )


def register():
    register_class(TeamsProperties)

    Scene.teams_properties = PointerProperty(type=TeamsProperties)


def unregister():
    unregister_class(TeamsProperties)

    del Scene.teams_properties
