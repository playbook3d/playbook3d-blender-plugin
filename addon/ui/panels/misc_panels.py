import bpy
from .panel_utils import PlaybookPanel, BOX_PADDING
from ..icons import icons


class ModificationPanel(PlaybookPanel, bpy.types.Panel):
    bl_idname = "SCENE_PT_modification"
    bl_label = ""
    bl_parent_id = "SCENE_PT_playbook"
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout
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


# The panel that creates the Playbook links
class LinksPanel(PlaybookPanel, bpy.types.Panel):
    bl_idname = "SCENE_PT_linkspanel"
    bl_parent_id = "SCENE_PT_playbook"
    bl_label = ""
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout

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
