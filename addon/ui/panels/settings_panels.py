import bpy
from .panel_utils import PlaybookPanel, create_label_row, BOX_PADDING, BUTTON_Y_SCALE


#
class RenderSettingsPanel(PlaybookPanel, bpy.types.Panel):
    bl_idname = "SCENE_PT_render_settings"
    bl_label = ""
    bl_parent_id = "SCENE_PT_playbook"
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()
        box.separator(factor=BOX_PADDING)

        # Workflow
        create_label_row(box, "Workflow")
        workflow_row = box.row()
        workflow_row.separator(factor=BOX_PADDING)
        workflow_row.template_icon_view(
            scene.general_properties,
            "general_workflow",
            show_labels=True,
            scale_popup=5,
        )
        workflow_row.separator(factor=BOX_PADDING)

        box.separator(factor=BOX_PADDING)

        # Style
        create_label_row(box, "Style")
        style_row = box.row()
        style_row.scale_y = 1.25
        style_row.separator(factor=BOX_PADDING)
        style_row.prop(scene.general_properties, "general_style")
        style_row.separator(factor=BOX_PADDING)

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

        box.separator(factor=BOX_PADDING)

        self.draw_mask_layout(scene, box)
        # Retexture panel
        # self.draw_retexture_layout(scene, layout)

        # Style Transfer panel
        # self.draw_style_layout(scene, layout)

        # Relight panel
        # self.draw_relight_layout(scene, layout)

        # Upscale panel
        # self.draw_upscale_layout(scene, layout)

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
            # self.draw_general_layout(scene, retexture_box)

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

            if scene.show_object_dropdown:
                drop_row = box.row()
                drop_row.scale_y = 1.25
                drop_row.separator(factor=BOX_PADDING)
                drop_row.prop(property, "object_dropdown", icon="OBJECT_DATA")
                drop_row.separator(factor=BOX_PADDING)
            else:
                box_row = box.row()
                box_row.scale_y = 0.25
                box_row.separator(factor=BOX_PADDING)
                drop_box = box_row.box()
                drop_box.scale_y = 0.25
                drop_box.separator(factor=BOX_PADDING)
                drop_box.label(
                    text=bpy.context.view_layer.objects.active.name, icon="OBJECT_DATA"
                )
                drop_box.separator(factor=BOX_PADDING)
                box_row.separator(factor=BOX_PADDING)
                box.separator(factor=1.4)

            box.separator()

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
            # Model
            create_label_row(upscale_box, "Model")
            model_row = upscale_box.row()
            model_row.separator(factor=BOX_PADDING)
            model_row.prop(scene.upscale_properties, "upscale_model")
            model_row.separator(factor=BOX_PADDING)

            # Value
            create_label_row(upscale_box, "Value")
            scale_row = upscale_box.row()
            scale_row.scale_y = 1
            scale_row.separator(factor=BOX_PADDING)
            scale_row.prop(scene.upscale_properties, "upscale_value")
            scale_row.separator(factor=BOX_PADDING)

            # Creativity
            create_label_row(upscale_box, "Creativity")
            creat_row = upscale_box.row()
            creat_row.separator(factor=BOX_PADDING)
            creat_row.prop(scene.upscale_properties, "upscale_creativity", slider=True)
            creat_row.separator(factor=BOX_PADDING)

            # Prompt
            create_label_row(upscale_box, "Prompt")
            prompt_row = upscale_box.row()
            prompt_row.separator(factor=BOX_PADDING)
            prompt_row.prop(scene.upscale_properties, "upscale_prompt")
            prompt_row.separator(factor=BOX_PADDING)

            upscale_box.separator(factor=BOX_PADDING)
