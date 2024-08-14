import bpy
from .panel_utils import PlaybookPanel, BOX_PADDING


# The panel that creates the render button
class RenderPanel(PlaybookPanel, bpy.types.Panel):
    bl_idname = "SCENE_PT_renderpanel"
    bl_parent_id = "SCENE_PT_playbook"
    bl_label = "Render Image"
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout

        box = layout.box()

        box.separator(factor=BOX_PADDING)

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
        column2.label(text="512 x 512")
        column2.label(text="5s")
        column2.label(text="2 credits")

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

        box.separator(factor=BOX_PADDING)
