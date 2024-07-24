import bpy


class PlaybookPanel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"


#
class MainPanel(PlaybookPanel, bpy.types.Panel):
    bl_label = "Playbook"
    bl_idname = "SCENE_PT_playbook"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Learn more about the Playbook plugin here.")


class GlobalPanel(PlaybookPanel, bpy.types.Panel):
    bl_label = "Global"
    bl_idname = "SCENE_PT_global"
    bl_parent_id = "SCENE_PT_playbook"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()

        # Prompt
        box.label(text="Prompt")
        box.prop(scene.global_properties, "global_prompt")

        # Style
        style_row = box.split(factor=0.2)
        style_row.label(text="Style")
        style_row.prop(scene.global_properties, "global_style")

        # Structure Strength
        box.label(text="Structure Strength")
        box.prop(scene.global_properties, "global_structure_strength", slider=True)


# The panel that shows the object render settings
class ObjectPanel(PlaybookPanel, bpy.types.Panel):
    bl_label = "Object"
    bl_idname = "SCENE_PT_object"
    bl_parent_id = "SCENE_PT_playbook"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        layout.label(text="Specify an object from the scene to guide the render.")


# class MaskPanel(PlaybookPanel, bpy.types.Panel):
#     bl_label = "Mask 1"
#     bl_idname = "SCENE_PT_maskpanel1"
#     bl_parent_id = "SCENE_PT_object"
#     bl_options = {"DEFAULT_CLOSED"}

#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene

#         # Prompt
#         mask_prompt_row = layout.split(factor=0.3)
#         mask_prompt_row.alignment = "RIGHT"
#         mask_prompt_row.label(text="Prompt")
#         mask_prompt_row.prop(scene.mask1_properties, "mask_prompt")

#         # Structure Strength
#         mask_strength_row = layout.split(factor=0.3)
#         mask_strength_row.alignment = "RIGHT"
#         mask_strength_row.label(text="Structure Strength")
#         mask_strength_row.prop(
#             scene.mask1_properties, "mask_structure_strength", slider=True
#         )

#         # Object Dropdown
#         object_dropdown_row = layout.split(factor=0.3)
#         object_dropdown_row.alignment = "RIGHT"
#         object_dropdown_row.label(text="Object Dropdown")
#         object_dropdown_row.prop(scene.mask1_properties, "object_dropdown")


# Creates and returns a panel for the mask layer for the given index
def create_mask_panel(index):
    class MaskPanel(PlaybookPanel, bpy.types.Panel):
        bl_label = f"Mask {index + 1}"
        bl_idname = f"SCENE_PT_maskpanel{index}"
        bl_parent_id = "SCENE_PT_object"
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

            # Mask Object
            layout.label(text="Mask Object")
            layout.prop(mask_property_index[index], "object_dropdown")

            # Prompt
            layout.label(text="Prompt")
            layout.prop(mask_property_index[index], "mask_prompt")

            # Style
            style_row = layout.split(factor=0.2)
            style_row.label(text="Style")
            style_row.prop(mask_property_index[index], "mask_style", slider=True)

            # Isolate
            layout.label(text="Isolate")
            layout.prop(mask_property_index[index], "mask_isolate", slider=True)

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
        layout.operator("object.render_image")
