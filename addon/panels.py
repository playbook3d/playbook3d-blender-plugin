import bpy


class PlaybookPanel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"


# The panel that shows the global render settings
class MainPanel(PlaybookPanel, bpy.types.Panel):
    bl_label = "Playbook"
    bl_idname = "SCENE_PT_playbook"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # RENDER SETTINGS
        layout.label(text="Render Settings")

        # Prompt
        prompt_row = layout.split(factor=0.3)
        prompt_row.alignment = "RIGHT"
        prompt_row.label(text="Prompt")
        prompt_row.prop(scene.render_properties, "global_prompt")

        # Structure Strength
        strength_row = layout.split(factor=0.3)
        strength_row.alignment = "RIGHT"
        strength_row.label(text="Structure Strength")
        strength_row.prop(
            scene.render_properties, "global_structure_strength", slider=True
        )


# Creates and returns a panel for the mask layer for the given index
def create_mask_panel(index):
    class MaskPanel(PlaybookPanel, bpy.types.Panel):
        bl_idname = f"SCENE_PT_maskpanel{index}"
        bl_parent_id = "SCENE_PT_playbook"
        bl_label = f"Mask Layer {index + 1}"
        bl_options = {"DEFAULT_CLOSED"}

        def draw(self, context):
            layout = self.layout
            scene = context.scene
            mask_property_index = [
                scene.mask_properties1,
                scene.mask_properties2,
                scene.mask_properties3,
                scene.mask_properties4,
                scene.mask_properties5,
                scene.mask_properties6,
                scene.mask_properties7,
            ]

            # Prompt
            mask_prompt_row = layout.split(factor=0.3)
            mask_prompt_row.alignment = "RIGHT"
            mask_prompt_row.label(text="Prompt")
            mask_prompt_row.prop(mask_property_index[index], "mask_prompt")

            # Structure Strength
            mask_strength_row = layout.split(factor=0.3)
            mask_strength_row.alignment = "RIGHT"
            mask_strength_row.label(text="Structure Strength")
            mask_strength_row.prop(
                mask_property_index[index], "mask_structure_strength", slider=True
            )

            # Object Dropdown
            list_row = layout.split(factor=0.3)
            list_row.alignment = "RIGHT"
            list_row.label(text="Object Dropdown")
            list_row.prop(mask_property_index[index], "object_dropdown")

            # Mask Layer Object List
            object_row = layout.split(factor=0.3)
            object_row.alignment = "RIGHT"
            object_row.label(text="Mask Objects")
            object_row.prop(mask_property_index[index], "object_list")

    return MaskPanel


# The panel that creates the render button
class RenderPanel(PlaybookPanel, bpy.types.Panel):
    bl_idname = "SCENE_PT_renderpanel"
    bl_parent_id = "SCENE_PT_playbook"
    bl_label = "Render Image"
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout

        layout.separator()

        render_row = layout.row()
        render_row.scale_y = 1.5
        render_row.operator("object.render_image")
