import bpy
from .panel_utils import PlaybookPanel3D, PlaybookPanelRender, BOX_PADDING
from ..icons import icons


########## MAIN PANEL ##########
def draw_main_panel(layout):
    row0 = layout.row()
    row1 = layout.row()

    row0.alignment = "CENTER"
    row1.alignment = "CENTER"

    row0.label(text="", icon_value=icons["main"]["playbook_logo_main"].icon_id)
    row1.label(text="Playbook")


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
def draw_credentials_panel(context, layout):
    scene = context.scene
    user_props = scene.user_properties

    box = layout.box()
    box.separator(factor=BOX_PADDING)

    row3 = box.row()
    row3.scale_y = 1.8
    row3.active_default = False if user_props.user_email else True
    row3.separator(factor=BOX_PADDING)
    login_text = (
        f"{user_props.user_email}"
        if user_props.user_email
        else "Enter API Key In Preferences"
    )
    row3.operator(
        "op.login",
        text=login_text,
    )
    row3.separator(factor=BOX_PADDING)

    row4 = box.row()
    row4.scale_y = 1.8
    row4.active_default = True if user_props.user_email else False
    row4.separator(factor=BOX_PADDING)
    row4.operator("op.dashboard")
    row4.separator(factor=BOX_PADDING)

    box.separator(factor=BOX_PADDING)


#
class CredentialsPanel3D(PlaybookPanel3D, bpy.types.Panel):
    bl_idname = "VIEW_3D_PT_credentials"
    bl_label = "Credentials"
    bl_parent_id = MainPanel3D.bl_idname
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        draw_credentials_panel(context, self.layout)


#
class CredentialsPanelRender(PlaybookPanelRender, bpy.types.Panel):
    bl_idname = "IMAGE_RENDER_PT_credentials"
    bl_label = "Credentials"
    bl_parent_id = MainPanelRender.bl_idname
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        draw_credentials_panel(context, self.layout)
