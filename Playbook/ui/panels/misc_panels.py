import bpy
from .panel_utils import PlaybookPanel3D, PlaybookPanelRender, BOX_PADDING
from .main_panels import MainPanel3D, MainPanelRender
from ..icons import icons


########## MODIFICATION PANEL ##########
def draw_modification_panel(context, layout):
    scene = context.scene
    flag_props = scene.flag_properties

    flags = [
        ("Retexture", flag_props.retexture_flag),
        ("Style Transfer", flag_props.style_flag),
        ("Relight", flag_props.relight_flag),
        ("Upscale", flag_props.upscale_flag),
    ]

    # Filter the flags that are active
    active_flags = [name for name, active in flags if active]

    if active_flags:
        row = layout.row()
        row.alignment = "CENTER"
        row.label(text="Applied:")

        row = layout.row()
        row.alignment = "CENTER"
        row.label(text=", ".join(active_flags))


#
class ModificationPanel3D(PlaybookPanel3D, bpy.types.Panel):
    bl_idname = "VIEW_3D_PT_modification"
    bl_label = ""
    bl_parent_id = MainPanel3D.bl_idname
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        draw_modification_panel(context, self.layout)


#
class ModificationPanelRender(PlaybookPanelRender, bpy.types.Panel):
    bl_idname = "IMAGE_RENDER_PT_modification"
    bl_label = ""
    bl_parent_id = MainPanelRender.bl_idname
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        draw_modification_panel(context, self.layout)


########## LINKS PANEL ##########
def draw_links_panel(layout):
    icon_row = layout.row()
    icon_row.alignment = "CENTER"
    icon_row.operator(
        "op.send_to_playbook",
        icon_value=icons["main"]["playbook_logo"].icon_id,
        emboss=False,
    )
    icon_row.operator(
        "op.send_to_discord",
        icon_value=icons["main"]["discord_logo"].icon_id,
        emboss=False,
    )
    icon_row.operator(
        "op.send_to_twitter",
        icon_value=icons["main"]["twitter_logo"].icon_id,
        emboss=False,
    )

    layout.separator(factor=BOX_PADDING)


# The panel that creates the Playbook links
class LinksPanel3D(PlaybookPanel3D, bpy.types.Panel):
    bl_idname = "VIEW_3D_PT_linkspanel"
    bl_label = ""
    bl_parent_id = MainPanel3D.bl_idname
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        draw_links_panel(self.layout)


#
class LinksPanelRender(PlaybookPanelRender, bpy.types.Panel):
    bl_idname = "IMAGE_RENDER_PT_linkspanel"
    bl_label = ""
    bl_parent_id = MainPanelRender.bl_idname
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        draw_links_panel(self.layout)
