import bpy
from .main_panels import MainPanel3D, MainPanelRender
from .panel_utils import (
    PlaybookPanel3D,
    PlaybookPanelRender,
    create_label_row,
    BOX_PADDING,
)


########## TEAMS PANEL ##########
def draw_teams_panel(context, layout):
    box = layout.box()
    box.separator(factor=BOX_PADDING)

    scene = context.scene
    user_properties = scene.user_properties

    create_label_row(box, "Team")
    teams_row = box.row()
    teams_row.scale_y = 1.25
    teams_row.separator(factor=BOX_PADDING)
    teams_row.prop(user_properties, "user_teams_dropdown")
    teams_row.separator(factor=BOX_PADDING)

    box.separator(factor=BOX_PADDING)

    create_label_row(box, "Workflow")
    workflows_row = box.row()
    workflows_row.scale_y = 1.25
    workflows_row.separator(factor=BOX_PADDING)
    workflows_row.prop(user_properties, "user_workflows_dropdown")
    workflows_row.separator(factor=BOX_PADDING)

    refresh_row = box.row()
    refresh_row.scale_y = 1.25
    refresh_row.separator(factor=BOX_PADDING)
    refresh_row.operator("op.refresh")
    refresh_row.separator(factor=BOX_PADDING)

    box.separator(factor=BOX_PADDING)


class TeamsPanel3D(PlaybookPanel3D, bpy.types.Panel):
    bl_idname = "VIEW_3D_PT_teamspanel"
    bl_label = "Teams Details"
    bl_parent_id = MainPanel3D.bl_idname
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        draw_teams_panel(context, self.layout)


class TeamsPanelRender(PlaybookPanelRender, bpy.types.Panel):
    bl_idname = "IMAGE_RENDER_PT_teamspanel"
    bl_label = "Teams Details"
    bl_parent_id = MainPanelRender.bl_idname
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        draw_teams_panel(context, self.layout)
