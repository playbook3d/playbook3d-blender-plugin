import bpy


BOX_PADDING = 0.1
BUTTON_Y_SCALE = 1.25
TEXT_Y_SCALE = 0.5


def create_label_row(layout, text, scale_y=TEXT_Y_SCALE):
    row = layout.row()
    row.scale_y = scale_y
    row.separator(factor=BOX_PADDING)
    row.label(text=text)
    row.separator(factor=BOX_PADDING)


class PlaybookPanel3D(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Playbook"


class PlaybookPanelRender(bpy.types.Panel):
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Playbook"
