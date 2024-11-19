import bpy
from .main_panels import MainPanel3D, MainPanelRender
from .panel_utils import PlaybookPanel3D, PlaybookPanelRender, BOX_PADDING


########## TEAMS PANEL ##########
def draw_teams_panel(context, layout):
    box = layout.box()
    box.separator(factor=BOX_PADDING)

    scene = context.scene
    teams_properties = scene.teams_properties

    column = box.column()
    column.scale_y = 1.75
    column.separator(factor=BOX_PADDING)
    column.label(text="Team")
    column.prop(teams_properties, "teams_dropdown")
    column.separator(factor=BOX_PADDING)

    column.separator(factor=BOX_PADDING)
    column.label(text="Project")
    column.prop(teams_properties, "projects_dropdown")
    column.separator(factor=BOX_PADDING)

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
