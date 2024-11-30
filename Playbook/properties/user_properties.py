import bpy
from bpy.props import PointerProperty, StringProperty, EnumProperty
from bpy.types import Scene, PropertyGroup
from bpy.utils import register_class, unregister_class

teams = ["None"]
projects = ["None"]


#
class UserProperties(PropertyGroup):
    def create_teams(self, context):
        return [(team.replace(" ", "").upper(), team, "") for team in teams]

    def create_projects(self, context):
        return [(project.replace(" ", "").upper(), project, "") for project in projects]

    def on_update_teams(self, context):
        print(self.teams_dropdown)

    def on_update_project(self, context):
        print(self.projects_dropdown)

    user_email: StringProperty(
        name="",
    )
    user_teams_dropdown: EnumProperty(
        name="",
        items=create_teams,
        update=lambda self, context: self.on_update_teams(context),
    )
    projects_dropdown: EnumProperty(
        name="",
        items=[],
        update=lambda self, context: self.on_update_project(context),
    )


def register():
    register_class(UserProperties)

    Scene.user_properties = PointerProperty(type=UserProperties)


def unregister():
    unregister_class(UserProperties)

    del Scene.user_properties


def update_user_properties(email: str, new_teams: list[str]):
    print(f"Updating: {email}, {new_teams[0]}")
    bpy.context.scene.user_properties.user_email = email

    global teams
    teams = new_teams
