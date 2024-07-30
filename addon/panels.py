import bpy
from .utilities import icons

BOX_PADDING = 0.1
BUTTON_Y_SCALE = 1.7


class PlaybookPanel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"


#
class MainPanel(PlaybookPanel, bpy.types.Panel):
    bl_idname = "SCENE_PT_playbook"
    bl_label = "Playbook"

    def draw(self, context):
        layout = self.layout
        layout.alignment = "CENTER"
        layout.label(text="Playbook is a diffusion based")
        layout.label(text="engine for 3D scenes.")


#
class CredentialsPanel(PlaybookPanel, bpy.types.Panel):
    bl_idname = "SCENE_PT_credentials"
    bl_label = "Credentials"
    bl_parent_id = "SCENE_PT_playbook"
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.separator(factor=BOX_PADDING)

        row1 = box.row()
        row1.scale_y = 1.8
        row1.separator(factor=BOX_PADDING)
        row1.operator("op.login", icon_value=icons["main"]["check_icon"].icon_id)
        row1.separator(factor=BOX_PADDING)

        row2 = box.row()
        row2.scale_y = 1.8
        row2.active_default = True
        row2.separator(factor=BOX_PADDING)
        row2.operator("op.upgrade")
        row2.separator(factor=BOX_PADDING)

        row3 = box.row()
        row3.alignment = "CENTER"
        row3.label(
            text="100 credits remaining",
            icon_value=icons["main"]["credit_icon"].icon_id,
        )

        box.separator(factor=BOX_PADDING)


#
class RenderSettingsPanel(PlaybookPanel, bpy.types.Panel):
    bl_idname = "SCENE_PT_render_settings"
    bl_label = ""
    bl_parent_id = "SCENE_PT_playbook"
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # General panel
        self.draw_retexture_layout(scene, layout)

        self.draw_style_layout(scene, layout)
        self.draw_relight_layout(scene, layout)
        self.draw_upscale_layout(scene, layout)

    #
    def draw_retexture_layout(self, scene, layout):
        retexture_row = layout.row()

        retexture_box = retexture_row.box()
        retexture_box.scale_y = BUTTON_Y_SCALE

        if not scene.show_retexture_panel:
            retexture_box.operator("op.retexture_panel", icon="PROP_OFF", emboss=False)
        else:
            retexture_box.operator("op.retexture_panel", icon="PROP_ON", emboss=False)

            self.draw_general_layout(scene, retexture_box)

            row = retexture_box.row()
            row.scale_y = 0.05
            row.label(text="")

            self.draw_mask_layout(scene, retexture_box)

    #
    def draw_general_layout(self, scene, box):
        retexture_column = box.column()

        # Prompt
        retexture_column.label(text="Prompt")
        retexture_column.prop(scene.general_properties, "general_prompt")
        retexture_column.operator("op.randomize_prompt")

        # Style
        retexture_column.label(text="Model")
        retexture_column.prop(scene.general_properties, "general_style")

        # Structure Strength
        retexture_column.label(text="Structure Strength")
        retexture_column.prop(
            scene.general_properties, "general_structure_strength", slider=True
        )

    #
    def draw_mask_layout(self, scene, box):
        mask_column = box.column()

        # Masks list
        mask_column.label(text="Masks")

        list_col = mask_column.column()
        list_col.scale_y = 0.5
        list_col.template_list(
            "PB_UL_CustomList", "", scene, "mask_list", scene, "mask_list_index"
        )

        list_row = mask_column.row()
        list_row.operator("list.add_mask_item", text="Add")
        list_row.operator("list.remove_mask_item", text="Remove")

        # Objects in mask list
        if scene.mask_list_index != -1:
            mask_column.label(text="Objects in Mask")

            property = getattr(scene, f"mask_properties{scene.mask_list_index + 1}")

            list_col = mask_column.column()
            list_col.scale_y = 0.5
            list_col.template_list(
                "PB_UL_CustomList",
                "",
                property,
                "mask_objects",
                property,
                "object_list_index",
            )

            list_row = mask_column.row()
            list_row.operator("list.add_mask_object_item", text="Add")
            list_row.operator("list.remove_mask_object_item", text="Remove")
            list_row.operator("list.clear_mask_object_list", text="Clear")

            mask_column.prop(property, "object_dropdown", icon="PROP_ON")

            mask_column.label(text="Prompt")
            mask_column.prop(property, "mask_prompt")

    #
    def draw_style_layout(self, scene, layout):
        style_row = layout.row()

        style_box = style_row.box()
        style_box.scale_y = BUTTON_Y_SCALE

        if not scene.show_style_panel:
            style_box.operator("op.style_panel", icon="PROP_OFF", emboss=False)
        else:
            style_box.operator("op.style_panel", icon="PROP_ON", emboss=False)
            style_column = style_box.column()

            style_column.prop(scene.style_properties, "style_image")

            style_column.label(text="Strength")
            style_column.prop(scene.style_properties, "style_strength", slider=True)

    #
    def draw_relight_layout(self, scene, layout):
        relight_row = layout.row()

        relight_box = relight_row.box()
        relight_box.scale_y = BUTTON_Y_SCALE

        if not scene.show_relight_panel:
            relight_box.operator("op.relight_panel", icon="PROP_OFF", emboss=False)
        else:
            relight_box.operator("op.relight_panel", icon="PROP_ON", emboss=False)
            relight_column = relight_box.column()

            row = relight_column.row()
            row.prop(scene.relight_properties, "relight_type", expand=True)

            if scene.is_relight_image:
                relight_column.prop(scene.relight_properties, "relight_image")
            else:
                relight_column.prop(scene.relight_properties, "relight_color")

            relight_column.label(text="Strength")
            relight_column.prop(
                scene.relight_properties, "relight_strength", slider=True
            )

    #
    def draw_upscale_layout(self, scene, layout):
        upscale_row = layout.row()

        upscale_box = upscale_row.box()
        upscale_box.scale_y = BUTTON_Y_SCALE

        if not scene.show_upscale_panel:
            upscale_box.operator("op.upscale_panel", icon="PROP_OFF", emboss=False)
        else:
            upscale_box.operator("op.upscale_panel", icon="PROP_ON", emboss=False)
            upscale_column = upscale_box.column()

            # Prompt
            upscale_column.label(text="Scale")
            upscale_column.prop(scene.upscale_properties, "upscale_scale")


# The panel that shows the object render settings
class ObjectPanel(PlaybookPanel, bpy.types.Panel):
    bl_idname = "SCENE_PT_object"
    bl_label = "Object"
    bl_parent_id = "SCENE_PT_playbook"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        layout.label(text="Specify an object from the scene to guide the render.")


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
        column1 = split.column()
        column1.alignment = "LEFT"
        column1.label(text="Final resolution:")
        column1.label(text="Estimated time:")
        column1.label(text="Credit cost:")
        row.separator(factor=BOX_PADDING)

        column2 = split.column()
        column2.alignment = "RIGHT"
        column2.label(text="512 x 512")
        column2.label(text="5s")
        column2.label(text="2 credits", icon_value=icons["main"]["credit_icon"].icon_id)

        row1 = box.row()
        row1.scale_y = BUTTON_Y_SCALE
        row1.separator(factor=BOX_PADDING)
        row1.operator("op.queue")
        row1.separator(factor=BOX_PADDING)

        row2 = box.row()
        row2.active_default = True
        row2.scale_y = BUTTON_Y_SCALE
        row2.separator(factor=BOX_PADDING)
        row2.operator("op.render_image")
        row2.separator(factor=BOX_PADDING)

        box.separator(factor=BOX_PADDING)


# The panel that creates the Playbook links
class LinksPanel(PlaybookPanel, bpy.types.Panel):
    bl_idname = "SCENE_PT_linkspanel"
    bl_parent_id = "SCENE_PT_playbook"
    bl_label = ""
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout

        split = layout.split(factor=1 / 3)
        col1 = split.column()
        col2 = split.column()
        col3 = split.column()

        icon_row = col2.row()
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
