import bpy
from bpy.props import PointerProperty, StringProperty, EnumProperty
from bpy.types import Scene, PropertyGroup
from bpy.utils import register_class, unregister_class
from .team_properties import TeamProperties
from .workflow_properties import WorkflowProperties


teams = [TeamProperties("0", "None")]
workflows = [WorkflowProperties("1", "0", "None")]


#
class UserProperties(PropertyGroup):
    def create_teams(self, context):
        return [(team.id, team.name, "") for team in teams]

    def create_workflows(self, context):
        current_team_id = self.user_teams_dropdown

        workflows_in_team = filter(
            lambda workflow: workflow.team_id == current_team_id, workflows
        )
        return [(workflow.id, workflow.name, "") for workflow in workflows_in_team]

    def on_update_teams(self, context):
        team = next(team for team in teams if team.id == self.user_teams_dropdown)
        print(f"Switching team to: {team.name}")

    def on_update_workflows(self, context):
        workflow = next(
            workflow
            for workflow in workflows
            if workflow.id == self.user_workflows_dropdown
        )
        print(f"Switching workflow to: {workflow.name}")

    user_email: StringProperty(
        name="",
    )
    user_teams_dropdown: EnumProperty(
        name="",
        items=create_teams,
        update=lambda self, context: self.on_update_teams(context),
    )
    user_workflows_dropdown: EnumProperty(
        name="",
        items=create_workflows,
        update=lambda self, context: self.on_update_workflows(context),
    )


def register():
    register_class(UserProperties)

    Scene.user_properties = PointerProperty(type=UserProperties)


def unregister():
    unregister_class(UserProperties)

    del Scene.user_properties


#
def update_user_properties(
    email: str,
    user_teams: list[TeamProperties],
    user_workflows: list[WorkflowProperties],
):
    bpy.context.scene.user_properties.user_email = email

    global teams, workflows
    teams = user_teams

    if user_workflows:
        workflows = user_workflows


#
def get_team_id_of_workflow(workflow_id: str) -> str:
    workflow = next(workflow for workflow in workflows if workflow.id == workflow_id)
    return workflow.team_id
