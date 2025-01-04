import bpy
from .main_panels import MainPanel3D, MainPanelRender
from ...render_status import RenderStatus
from .panel_utils import PlaybookPanel3D, BOX_PADDING, PlaybookPanelRender


########## RENDER PANEL ##########
def draw_render_panel(context, layout):
    box = layout.box()
    box.separator(factor=BOX_PADDING)

    render_properties = context.scene.render_properties
    scene = context.scene

    row0 = box.row()
    row0.scale_y = 1.75
    row0.separator(factor=BOX_PADDING)
    row0.operator("op.capture_passes")
    row0.separator(factor=BOX_PADDING)

    row1 = box.row()
    row1.scale_y = 1.75
    row1.active_default = True
    row1.separator(factor=BOX_PADDING)
    row1.operator("op.single_image_capture")
    row1.separator(factor=BOX_PADDING)

    box.separator(factor=BOX_PADDING)
    box.separator(factor=BOX_PADDING)

    row2 = box.row()
    row2.scale_y = 1.75
    row2.active_default = False if render_properties.is_capturing_sequence else True
    row2.separator(factor=BOX_PADDING)
    row2.operator("op.start_sequence_capture")
    row2.separator(factor=BOX_PADDING)

    row3 = box.row()
    row3.scale_y = 1.75
    row3.active_default = True if render_properties.is_capturing_sequence else False
    row3.separator(factor=BOX_PADDING)
    row3.operator("op.end_sequence_capture")
    row3.separator(factor=BOX_PADDING)

    if scene.status_message:
        row_label = box.row()
        row_label.alignment = "CENTER"
        row_label.label(text=scene.status_message)

    if scene.error_message:
        error_row = box.row()
        error_row.alert = True
        error_row.alignment = "CENTER"
        error_row.separator(factor=BOX_PADDING)
        error_row.label(
            text=scene.error_message,
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
