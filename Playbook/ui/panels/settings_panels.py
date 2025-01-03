import bpy
from .main_panels import MainPanel3D, MainPanelRender
from .panel_utils import (
    PlaybookPanel3D,
    PlaybookPanelRender,
    create_label_row,
    BOX_PADDING,
)


########## ADVANCED SETTINGS PANEL ##########
def draw_advanced_settings_panel(context, layout):
    scene = context.scene

    box = layout.box()
    box.separator(factor=BOX_PADDING)

    draw_checkbox_layout(scene, box)
    draw_mask_layout(scene, box)


#
def draw_checkbox_layout(scene, box):
    render_properties = scene.render_properties

    create_label_row(box, "Render Passes", 0.75)

    checkbox_row = box.row()
    checkbox_row.separator(factor=BOX_PADDING)

    checkbox_col = checkbox_row.column()
    checkbox_col.separator(factor=BOX_PADDING)
    checkbox_col.prop(render_properties, "beauty_pass_checkbox")
    checkbox_col.prop(render_properties, "mask_pass_checkbox")
    checkbox_col.prop(render_properties, "outline_pass_checkbox")
    checkbox_col.prop(render_properties, "normal_pass_checkbox")
    checkbox_col.separator(factor=BOX_PADDING)

    checkbox_row.separator(factor=BOX_PADDING)

    box.separator(factor=BOX_PADDING)


#
def draw_mask_layout(scene, box):
    property = getattr(scene, f"mask_properties{scene.mask_list_index + 1}")

    # Masks list
    create_label_row(box, "Masks", 0.75)

    list_row = box.row()
    list_row.separator(factor=BOX_PADDING)
    list_row.template_list(
        "PB_UL_CustomList",
        "Mask List",
        scene,
        "mask_list",
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

        create_label_row(box, "Objects in Mask", 0.75)

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

    box.separator(factor=BOX_PADDING)


#
class AdvancedSettingsPanel3D(PlaybookPanel3D, bpy.types.Panel):
    bl_idname = "VIEW_3D_PT_advanced_settings"
    bl_label = "Adjust Render Passes"
    bl_parent_id = MainPanel3D.bl_idname
    bl_options = {"HEADER_LAYOUT_EXPAND"}

    def draw(self, context):
        draw_advanced_settings_panel(context, self.layout)


#
class AdvancedSettingsPanelRender(PlaybookPanelRender, bpy.types.Panel):
    bl_idname = "IMAGE_RENDER_PT_advanced_settings"
    bl_label = "Adjust Render Passes"
    bl_parent_id = MainPanelRender.bl_idname
    bl_options = {"HEADER_LAYOUT_EXPAND"}

    def draw(self, context):
        draw_advanced_settings_panel(context, self.layout)
