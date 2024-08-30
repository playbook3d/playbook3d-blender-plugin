import bpy
from .main_panels import MainPanel3D, MainPanelRender
from ...properties import render_stats
from .panel_utils import PlaybookPanel3D, BOX_PADDING, PlaybookPanelRender


########## RENDER PANEL ##########
def draw_render_panel(context, layout):
    box = layout.box()
    box.separator(factor=BOX_PADDING)

    model = context.scene.global_properties.global_model

    row = box.row()
    row.separator(factor=BOX_PADDING)
    split = row.split()
    column1 = split.column(align=True)
    column1.alignment = "LEFT"
    column1.label(text="Final resolution:")
    column1.label(text="Estimated time:")
    column1.label(text="Credit cost:")
    row.separator(factor=BOX_PADDING)

    column2 = split.column(align=True)
    column2.alignment = "RIGHT"
    column2.label(text=render_stats[model]["Resolution"])
    column2.label(text=render_stats[model]["Time"])
    column2.label(text=render_stats[model]["Cost"])

    row1 = box.row()
    row1.scale_y = 1.75
    row1.separator(factor=BOX_PADDING)
    row1.operator("op.queue")
    row1.separator(factor=BOX_PADDING)

    row2 = box.row()
    row2.scale_y = 1.75
    row2.active_default = True
    row2.separator(factor=BOX_PADDING)
    row2.operator("op.render_image")
    row2.separator(factor=BOX_PADDING)

    if context.scene.is_rendering:
        row_label = box.row()
        row_label.alignment = "CENTER"
        row_label.label(text="Generating...")

    if context.scene.error_message:
        error_row = box.row()
        error_row.alert = True
        error_row.alignment = "CENTER"
        error_row.separator(factor=BOX_PADDING)
        error_row.label(
            text=context.scene.error_message,
        )
        error_row.separator(factor=BOX_PADDING)

    box.separator(factor=BOX_PADDING)


# The panel that creates the render button
class RenderPanel3D(PlaybookPanel3D, bpy.types.Panel):
    bl_idname = "VIEW_3D_PT_renderpanel"
    bl_label = "Render Image"
    bl_parent_id = MainPanel3D.bl_idname
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        draw_render_panel(context, self.layout)


# The panel that creates the render button
class RenderPanelRender(PlaybookPanelRender, bpy.types.Panel):
    bl_idname = "IMAGE_RENDER_PT_renderpanel"
    bl_label = "Render Image"
    bl_parent_id = MainPanelRender.bl_idname
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        draw_render_panel(context, self.layout)
