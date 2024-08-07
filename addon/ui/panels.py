import bpy
from bpy.utils import register_class, unregister_class
from bpy.props import BoolProperty
from bpy.types import Scene
from .icons import icons

BOX_PADDING = 0.1
BUTTON_Y_SCALE = 1.25
TEXT_Y_SCALE = 0.5


def create_label_row(layout, text, scale_y=TEXT_Y_SCALE):
    row = layout.row()
    row.scale_y = scale_y
    row.separator(factor=BOX_PADDING)
    row.label(text=text)
    row.separator(factor=BOX_PADDING)


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
        row2.label(text="Playbook is a diffusion based")
        row3.label(text="engine for 3D scenes.")


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
        row3.label(
            text="100 credits remaining",
            icon_value=icons["main"]["credit_icon"].icon_id,
        )

        box.separator(factor=BOX_PADDING)


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


#
class RenderSettingsPanel(PlaybookPanel, bpy.types.Panel):
    bl_idname = "SCENE_PT_render_settings"
    bl_label = ""
    bl_parent_id = "SCENE_PT_playbook"
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Retexture panel
        self.draw_retexture_layout(scene, layout)

        # Style Transfer panel
        self.draw_style_layout(scene, layout)

        # Relight panel
        self.draw_relight_layout(scene, layout)

        # Upscale panel
        self.draw_upscale_layout(scene, layout)

    #
    def draw_retexture_layout(self, scene, layout):
        retexture_box = layout.box()
        retexture_row = retexture_box.row()

        retexture_row.scale_y = BUTTON_Y_SCALE
        retexture_row.operator(
            "op.retexture_panel",
            icon="PROP_ON" if scene.show_retexture_panel else "PROP_OFF",
            emboss=False,
        )

        if scene.show_retexture_panel:
            self.draw_general_layout(scene, retexture_box)

            retexture_box.separator(factor=2)

            self.draw_mask_layout(scene, retexture_box)

    #
    def draw_general_layout(self, scene, box):
        # Prompt
        create_label_row(box, "Scene Prompt")

        prompt_row = box.row()
        prompt_row.scale_y = 1.25
        prompt_row.separator(factor=BOX_PADDING)
        prompt_row.prop(scene.general_properties, "general_prompt")
        prompt_row.separator(factor=BOX_PADDING)

        randomize_row = box.row()
        randomize_row.scale_y = 1.25
        randomize_row.separator(factor=BOX_PADDING)
        randomize_row.operator("op.randomize_prompt")
        randomize_row.separator(factor=BOX_PADDING)

        box.separator(factor=BOX_PADDING)

        # Model
        create_label_row(box, "Model")

        model_row = box.row()
        model_row.scale_y = 1.25
        model_row.separator(factor=BOX_PADDING)
        model_row.prop(scene.general_properties, "general_style")
        model_row.separator(factor=BOX_PADDING)

        box.separator(factor=BOX_PADDING)

        # Structure Strength
        create_label_row(box, "Structure Strength")

        strength_row = box.row()
        strength_row.scale_y = 1.25
        strength_row.separator(factor=BOX_PADDING)
        strength_row.prop(
            scene.general_properties, "general_structure_strength", slider=True
        )
        strength_row.separator(factor=BOX_PADDING)

    #
    def draw_mask_layout(self, scene, box):
        # Masks list
        create_label_row(box, "Masks")

        list_row = box.row()
        list_row.separator(factor=BOX_PADDING)
        list_row.template_list(
            "PB_UL_CustomList",
            "",
            scene,
            "mask_list",
            scene,
            "mask_list_index",
            sort_lock=True,
        )
        list_row.separator(factor=BOX_PADDING)

        list_row = box.row()
        list_row.scale_y = 1.25
        list_row.separator(factor=BOX_PADDING)
        list_row.operator("list.add_mask_item", text="Add")
        list_row.operator("list.remove_mask_item", text="Remove")
        list_row.separator(factor=BOX_PADDING)

        # Objects in mask list
        if scene.mask_list_index != -1:
            box.separator()

            create_label_row(box, "Objects in Mask")

            property = getattr(scene, f"mask_properties{scene.mask_list_index + 1}")

            list_row = box.row()
            list_row.separator(factor=BOX_PADDING)
            list_row.template_list(
                "PB_UL_CustomList",
                "",
                property,
                "mask_objects",
                property,
                "object_list_index",
                sort_lock=True,
            )
            list_row.separator(factor=BOX_PADDING)

            op_row = box.row()
            op_row.scale_y = 1.25
            op_row.separator(factor=BOX_PADDING)
            op_row.operator("list.add_mask_object_item", text="Add")
            op_row.operator("list.remove_mask_object_item", text="Remove")
            op_row.operator("list.clear_mask_object_list", text="Clear")
            op_row.separator(factor=BOX_PADDING)

            drop_row = box.row()
            drop_row.scale_y = 1.25
            drop_row.separator(factor=BOX_PADDING)
            drop_row.prop(property, "object_dropdown", icon="OBJECT_DATA")
            drop_row.separator(factor=BOX_PADDING)

            # Prompt
            create_label_row(box, "Mask Prompt")
            prompt_row = box.row()
            prompt_row.scale_y = 1.25
            prompt_row.separator(factor=BOX_PADDING)
            prompt_row.prop(property, "mask_prompt")
            prompt_row.separator(factor=BOX_PADDING)

        box.separator(factor=BOX_PADDING)

    #
    def draw_style_layout(self, scene, layout):
        style_box = layout.box()
        style_box.scale_y = BUTTON_Y_SCALE
        style_box.operator(
            "op.style_panel",
            icon="PROP_ON" if scene.show_style_panel else "PROP_OFF",
            emboss=False,
        )

        if scene.show_style_panel:
            image_row = style_box.row()
            image_row.scale_y = 1
            image_row.separator(factor=BOX_PADDING)
            image_row.prop(scene.style_properties, "style_image")
            image_row.operator("op.clear_style_image", icon="PANEL_CLOSE")
            image_row.separator(factor=BOX_PADDING)

            create_label_row(style_box, "Strength")

            strength_row = style_box.row()
            strength_row.scale_y = 1
            strength_row.separator(factor=BOX_PADDING)
            strength_row.prop(scene.style_properties, "style_strength", slider=True)
            strength_row.separator(factor=BOX_PADDING)

            style_box.separator(factor=BOX_PADDING)

    #
    def draw_relight_layout(self, scene, layout):
        relight_row = layout.row()

        relight_box = relight_row.box()
        relight_box.scale_y = BUTTON_Y_SCALE
        relight_box.operator(
            "op.relight_panel",
            icon="PROP_ON" if scene.show_relight_panel else "PROP_OFF",
            emboss=False,
        )

        if scene.show_relight_panel:
            type_row = relight_box.row()
            type_row.separator(factor=BOX_PADDING)
            type_row.prop(scene.relight_properties, "relight_type", expand=True)
            type_row.separator(factor=BOX_PADDING)

            if scene.is_relight_image:
                image_row = relight_box.row()
                image_row.scale_y = 1
                image_row.separator(factor=BOX_PADDING)
                image_row.prop(scene.relight_properties, "relight_image")
                image_row.operator("op.clear_relight_image", icon="PANEL_CLOSE")
                image_row.separator(factor=BOX_PADDING)
            else:
                color_row = relight_box.row()
                color_row.scale_y = 1
                color_row.separator(factor=BOX_PADDING)
                color_row.prop(scene.relight_properties, "relight_color")
                color_row.separator(factor=BOX_PADDING)

            # Angle
            create_label_row(relight_box, "Angle")
            angle_row = relight_box.row()
            angle_row.scale_y = 1
            angle_row.separator(factor=BOX_PADDING)
            angle_row.prop(scene.relight_properties, "relight_angle")
            angle_row.separator(factor=BOX_PADDING)

            # Prompt
            create_label_row(relight_box, "Prompt")
            prompt_row = relight_box.row()
            prompt_row.scale_y = 1
            prompt_row.separator(factor=BOX_PADDING)
            prompt_row.prop(scene.relight_properties, "relight_prompt")
            prompt_row.separator(factor=BOX_PADDING)

            # Strength
            create_label_row(relight_box, "Strength")
            strength_row = relight_box.row()
            strength_row.scale_y = 1
            strength_row.separator(factor=BOX_PADDING)
            strength_row.prop(scene.relight_properties, "relight_strength", slider=True)
            strength_row.separator(factor=BOX_PADDING)

            relight_box.separator(factor=BOX_PADDING)

    #
    def draw_upscale_layout(self, scene, layout):
        upscale_box = layout.box()

        upscale_box.scale_y = BUTTON_Y_SCALE
        upscale_box.operator(
            "op.upscale_panel",
            icon="PROP_ON" if scene.show_upscale_panel else "PROP_OFF",
            emboss=False,
        )

        if scene.show_upscale_panel:
            # Prompt
            create_label_row(upscale_box, "Scale")
            scale_row = upscale_box.row()
            scale_row.scale_y = 1
            scale_row.separator(factor=BOX_PADDING)
            scale_row.prop(scene.upscale_properties, "upscale_scale")
            scale_row.separator(factor=BOX_PADDING)

            upscale_box.separator(factor=BOX_PADDING)


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


classes = [
    MainPanel,
    CredentialsPanel,
    ModificationPanel,
    RenderSettingsPanel,
    RenderPanel,
    LinksPanel,
]


def register():
    global classes
    for cls in classes:
        register_class(cls)

    Scene.show_retexture_panel = BoolProperty(default=False)
    Scene.show_mask_panel = BoolProperty(default=False)
    Scene.show_style_panel = BoolProperty(default=False)
    Scene.show_relight_panel = BoolProperty(default=False)
    Scene.is_relight_image = BoolProperty(default=True)
    Scene.show_upscale_panel = BoolProperty(default=False)


def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)

    del Scene.show_retexture_panel
    del Scene.show_mask_panel
    del Scene.show_style_panel
    del Scene.show_relight_panel
    del Scene.is_relight_image
    del Scene.show_upscale_panel
