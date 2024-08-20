import bpy
from .panel_utils import PlaybookPanel3D, PlaybookPanelRender, BOX_PADDING
from ..icons import icons


########## MAIN PANEL ##########
def draw_main_panel(layout):
    row0 = layout.row()
    row1 = layout.row()
    row2 = layout.row()
    row3 = layout.row()

    row0.alignment = "CENTER"
    row1.alignment = "CENTER"
    row2.alignment = "CENTER"
    row3.alignment = "CENTER"

    row2.scale_y = 0.5
    row3.scale_y = 0.5

    row0.label(text="", icon_value=icons["main"]["playbook_logo_main"].icon_id)
    row1.label(text="Playbook")
    row2.label(text="Playbook is the best way for 3D artists")
    row3.label(text="to leverage ComfyUI.")


#
class MainPanel3D(PlaybookPanel3D, bpy.types.Panel):
    bl_idname = "VIEW_3D_PT_playbook"
    bl_label = "Playbook"

    def draw(self, context):
        draw_main_panel(self.layout)


#
class MainPanelRender(PlaybookPanelRender, bpy.types.Panel):
    bl_idname = "IMAGE_RENDER_PT_playbook"
    bl_label = "Playbook"

    def draw(self, context):
        draw_main_panel(self.layout)


########## CREDENTIALS PANEL ##########
def draw_credentials_panel(layout):
    box = layout.box()
    box.separator(factor=BOX_PADDING)

    row1 = box.row()
    row1.scale_y = 1.8
    row1.separator(factor=BOX_PADDING)
    row1.operator("op.login", text="✓ skylar@playbookxr.com")
    row1.separator(factor=BOX_PADDING)

    row2 = box.row()
    row2.scale_y = 1.8
    row2.active_default = True
    row2.separator(factor=BOX_PADDING)
    row2.operator("op.upgrade")
    row2.separator(factor=BOX_PADDING)

    row3 = box.row()
    row3.alignment = "CENTER"
    row3.label(text="100 credits remaining")

    box.separator(factor=BOX_PADDING)


#
class CredentialsPanel3D(PlaybookPanel3D, bpy.types.Panel):
    bl_idname = "VIEW_3D_PT_credentials"
    bl_label = "Credentials"
    bl_parent_id = MainPanel3D.bl_idname
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        draw_credentials_panel(self.layout)


#
class CredentialsPanelRender(PlaybookPanelRender, bpy.types.Panel):
    bl_idname = "IMAGE_RENDER_PT_credentials"
    bl_label = "Credentials"
    bl_parent_id = MainPanelRender.bl_idname
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        draw_credentials_panel(self.layout)
