import bpy
from .main_panels import MainPanel3D, MainPanelRender
from ...properties import get_render_type
from ...utilities import is_valid_image_file
from .panel_utils import (
    PlaybookPanel3D,
    PlaybookPanelRender,
    create_label_row,
    BOX_PADDING,
)


########## RENDER SETTTINGS PANEL ##########
def draw_render_settings_panel(context, layout):
    scene = context.scene

    box = layout.box()
    box.separator(factor=BOX_PADDING)

    # Global layout
    draw_global_layout(scene, box)

    box.separator(factor=BOX_PADDING)

    # Retexture workflow
    if scene.show_retexture_panel:
        # Prompt
        create_label_row(box, "Scene Prompt")
        prompt_row = box.row()
        prompt_row.scale_y = 1.25
        prompt_row.separator(factor=BOX_PADDING)
        prompt_row.prop(scene.retexture_properties, "retexture_prompt")
        prompt_row.separator(factor=BOX_PADDING)

    # Style transfer workflow
    else:
        style_props = scene.style_properties

        # Style transfer image
        create_label_row(box, "Style Transfer Image")
        image_row = box.row()
        image_row.separator(factor=BOX_PADDING)
        row = image_row.split(factor=0.9)
        row.prop(style_props, "style_image")
        row.operator("op.clear_style_transfer_image", icon="PANEL_CLOSE")

        # Invalid file type
        if style_props.style_image and not is_valid_image_file(style_props.style_image):
            label_row = box.row()
            label_row.alert = True
            label_row.separator(factor=BOX_PADDING)
            label_row.label(text="Invalid file type. Please select an image.")
            label_row.separator(factor=BOX_PADDING)

        image_row.separator(factor=BOX_PADDING)

    box.separator(factor=BOX_PADDING)


def draw_global_layout(scene, box):
    # Workflow
    create_label_row(box, "Workflow")
    workflow_row = box.row()
    workflow_row.scale_y = 1.25
    workflow_row.separator(factor=BOX_PADDING)
    workflow_row.prop(scene.global_properties, "global_workflow")
    workflow_row.separator(factor=BOX_PADDING)

    box.separator(factor=BOX_PADDING)

    # Base Model
    create_label_row(box, "Base Model")
    model_row = box.row()
    model_row.scale_y = 1.25
    model_row.separator(factor=BOX_PADDING)
    model_row.prop(scene.global_properties, "global_model")
    model_row.separator(factor=BOX_PADDING)

    box.separator(factor=BOX_PADDING)

    # Style
    create_label_row(box, "Style")
    style_row = box.row()
    style_row.scale_y = 1.25
    style_row.separator(factor=BOX_PADDING)
    style_row.prop(scene.global_properties, "global_style")
    style_row.separator(factor=BOX_PADDING)


#
class RenderSettingsPanel3D(PlaybookPanel3D, bpy.types.Panel):
    bl_idname = "VIEW_3D_PT_render_settings"
    bl_label = ""
    bl_parent_id = MainPanel3D.bl_idname
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        draw_render_settings_panel(context, self.layout)


#
class RenderSettingsPanelRender(PlaybookPanelRender, bpy.types.Panel):
    bl_idname = "IMAGE_RENDER_PT_render_settings"
    bl_label = ""
    bl_parent_id = MainPanelRender.bl_idname
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        draw_render_settings_panel(context, self.layout)


########## ADVANCED SETTINGS PANEL ##########
def draw_advanced_settings_panel(context, layout):
    scene = context.scene

    box = layout.box()
    box.separator(factor=BOX_PADDING)

    # Structure Strength
    if scene.show_retexture_panel:
        create_label_row(box, "Structure Strength")
        strength_row = box.row()
        strength_row.scale_y = 1.25
        strength_row.separator(factor=BOX_PADDING)
        strength_row.prop(
            scene.retexture_properties, "retexture_structure_strength", slider=True
        )
        strength_row.separator(factor=BOX_PADDING)

        box.separator(factor=BOX_PADDING)

        if scene.global_properties.global_model != "FLUX":
            draw_mask_layout(scene, box)

    # Structure Strength
    else:
        create_label_row(box, "Style Transfer Strength")
        strength_row = box.row()
        strength_row.scale_y = 1.25
        strength_row.separator(factor=BOX_PADDING)
        strength_row.prop(scene.style_properties, "style_strength", slider=True)
        strength_row.separator(factor=BOX_PADDING)

        box.separator(factor=BOX_PADDING)


#
def draw_mask_layout(scene, box):
    render_type = get_render_type()
    property = getattr(
        scene, f"{render_type}_mask_properties{scene.mask_list_index + 1}"
    )

    # Masks list
    create_label_row(box, "Masks")

    list_row = box.row()
    list_row.separator(factor=BOX_PADDING)
    list_row.template_list(
        "PB_UL_CustomList",
        "Mask List",
        scene,
        f"{render_type}_mask_list",
        scene,
        "mask_list_index",
        sort_lock=True,
    )
    list_row.separator(factor=BOX_PADDING)

    rename_row = box.row()
    rename_row.separator(factor=BOX_PADDING)
    rename_row.label(text="Rename Mask")
    rename_row.prop(property, "mask_name")
    rename_row.separator(factor=BOX_PADDING)

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

        list_row = box.row()
        list_row.separator(factor=BOX_PADDING)
        list_row.template_list(
            "PB_UL_CustomList",
            "Object List",
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
            box_row.separator(factor=BOX_PADDING)
            drop_box = box_row.box()
            drop_box.scale_y = 0.35
            drop_box.separator(factor=BOX_PADDING)
            selected_objects = [obj.name for obj in bpy.context.selected_objects]
            drop_box.label(text=", ".join(selected_objects), icon="OBJECT_DATA")
            drop_box.separator(factor=BOX_PADDING)
            box_row.separator(factor=BOX_PADDING)

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
class AdvancedSettingsPanel3D(PlaybookPanel3D, bpy.types.Panel):
    bl_idname = "VIEW_3D_PT_advanced_settings"
    bl_label = "Advanced"
    bl_parent_id = RenderSettingsPanel3D.bl_idname
    bl_options = {"HEADER_LAYOUT_EXPAND"}

    def draw(self, context):
        draw_advanced_settings_panel(context, self.layout)


#
class AdvancedSettingsPanelRender(PlaybookPanelRender, bpy.types.Panel):
    bl_idname = "IMAGE_RENDER_PT_advanced_settings"
    bl_label = "Advanced"
    bl_parent_id = RenderSettingsPanelRender.bl_idname
    bl_options = {"HEADER_LAYOUT_EXPAND"}

    def draw(self, context):
        draw_advanced_settings_panel(context, self.layout)
