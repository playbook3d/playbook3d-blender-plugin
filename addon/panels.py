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
        row1.operator("op.login")
        row1.separator(factor=BOX_PADDING)

        row2 = box.row()
        row2.scale_y = 1.8
        row2.separator(factor=BOX_PADDING)
        row2.operator("op.credits")
        row2.separator(factor=BOX_PADDING)

        row3 = box.row()
        row3.alignment = "CENTER"
        row3.label(
            text="100 credits remaining",
            icon_value=icons["main"]["credit_icon"].icon_id,
        )

        box.separator(factor=BOX_PADDING)


class RenderSettingsPanel(PlaybookPanel, bpy.types.Panel):
    bl_idname = "SCENE_PT_render_settings"
    bl_label = ""
    bl_parent_id = "SCENE_PT_playbook"
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # General panel
        self.draw_general_layout(scene, layout)

        # Object mask panel
        self.draw_mask_layout(scene, layout)

        self.draw_style_layout(scene, layout)
        self.draw_relight_layout(scene, layout)
        self.draw_upscale_layout(scene, layout)

    #
    def draw_general_layout(self, scene, layout):
        general_row = layout.row()

        general_box = general_row.box()
        general_box.scale_y = BUTTON_Y_SCALE

        if not scene.show_general_panel:
            general_box.operator("op.general_panel", icon="PROP_OFF", emboss=False)
        else:
            general_box.operator("op.general_panel", icon="PROP_ON", emboss=False)
            general_column = general_box.column()

            # Prompt
            general_column.label(text="Prompt")
            general_column.prop(scene.general_properties, "general_prompt")
            general_column.operator("op.randomize_prompt")

            # Style
            general_column.label(text="Model")
            general_column.prop(scene.general_properties, "general_style")

            # Structure Strength
            general_column.label(text="Structure Strength")
            general_column.prop(
                scene.general_properties, "general_structure_strength", slider=True
            )

    #
    def draw_mask_layout(self, scene, layout):
        mask_properties = [
            scene.mask_properties1,
            scene.mask_properties2,
            scene.mask_properties3,
            scene.mask_properties4,
            scene.mask_properties5,
            scene.mask_properties6,
            scene.mask_properties7,
        ]
        show_mask = [
            scene.show_mask_properties1,
            scene.show_mask_properties2,
            scene.show_mask_properties3,
            scene.show_mask_properties4,
            scene.show_mask_properties5,
            scene.show_mask_properties6,
            scene.show_mask_properties7,
        ]

        mask_row = layout.row()

        mask_box = mask_row.box()
        mask_box.scale_y = BUTTON_Y_SCALE

        if not scene.show_mask_panel:
            mask_box.operator("op.object_mask_panel", icon="PROP_OFF", emboss=False)
        else:
            mask_box.operator("op.object_mask_panel", icon="PROP_ON", emboss=False)
            mask_column = mask_box.column()

            list_col = mask_column.column()
            list_col.scale_y = 0.5
            list_col.template_list(
                "PB_UL_CustomList", "", scene, "mask_list", scene, "mask_list_index"
            )

            list_row = mask_column.row()
            list_row.operator("list.add_mask_item", text="Add")
            list_row.operator("list.remove_mask_item", text="Remove")

            mask_column.label(text="Mask Objects")

            list_col = mask_column.column()
            list_col.scale_y = 0.5
            list_col.template_list(
                "PB_UL_CustomList",
                "",
                scene.mask_properties1,
                "mask_objects",
                scene.mask_properties1,
                "object_list_index",
            )

            list_row = mask_column.row()
            list_row.operator("list.add_mask_object_item", text="Add")

            mask_column.label(text="Prompt")
            mask_column.prop(scene.mask_properties1, "mask_prompt")

            # for index, (properties, show_mask) in enumerate(
            #     zip(mask_properties, show_mask)
            # ):
            #     mask_column.operator(f"op.mask_property_panel{index + 1}")

            #     if show_mask:
            #         # Mask Object
            #         mask_column.label(text="Mask Object")
            #         mask_column.prop(properties, "object_dropdown")

            #         # Prompt
            #         mask_column.label(text="Prompt")
            #         mask_column.prop(properties, "mask_prompt")

            #         # Style
            #         style_row = mask_column.split(factor=0.2)
            #         style_row.label(text="Style")
            #         style_row.prop(properties, "mask_style", slider=True)

            #         # Isolate
            #         mask_column.label(text="Isolate")
            #         mask_column.prop(properties, "mask_isolate", slider=True)

            #         mask_column.separator(factor=BOX_PADDING)

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
