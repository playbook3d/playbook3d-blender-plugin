import bpy

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

        layout.label(text="Playbook is a diffusion based engine for 3D scenes.")


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

        box.separator(factor=BOX_PADDING)


class GlobalPanel(PlaybookPanel, bpy.types.Panel):
    bl_idname = "SCENE_PT_global"
    bl_label = "Global"
    bl_parent_id = "SCENE_PT_playbook"
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        box = layout.box()

        box.separator(factor=BOX_PADDING)

        # Global panel
        global_row = box.row()
        global_row.separator(factor=BOX_PADDING)
        global_row.scale_y = BUTTON_Y_SCALE
        global_row.operator("op.global_panel")
        global_row.separator(factor=BOX_PADDING)

        if scene.show_global_panel:
            self.draw_global_layout(scene, box)

        # Object mask panel
        mask_row = box.row()
        mask_row.separator(factor=BOX_PADDING)
        mask_row.scale_y = BUTTON_Y_SCALE
        mask_row.operator("op.object_mask_panel")
        mask_row.separator(factor=BOX_PADDING)

        if scene.show_mask_panel:
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

            for index, (prop, show) in enumerate(zip(mask_properties, show_mask)):
                self.draw_mask_layout(box, prop, show, index)

        box.separator(factor=BOX_PADDING)

    #
    def draw_global_layout(self, scene, box):
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

    #
    def draw_mask_layout(self, box, properties, show_mask, index):
        box.operator(f"op.mask_property_panel{index + 1}")

        if show_mask:
            # Mask Object
            box.label(text="Mask Object")
            box.prop(properties, "object_dropdown")

            # Prompt
            box.label(text="Prompt")
            box.prop(properties, "mask_prompt")

            # Style
            style_row = box.split(factor=0.2)
            style_row.label(text="Style")
            style_row.prop(properties, "mask_style", slider=True)

            # Isolate
            box.label(text="Isolate")
            box.prop(properties, "mask_isolate", slider=True)


# The panel that shows the object render settings
class ObjectPanel(PlaybookPanel, bpy.types.Panel):
    bl_idname = "SCENE_PT_object"
    bl_label = "Object"
    bl_parent_id = "SCENE_PT_playbook"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        layout.label(text="Specify an object from the scene to guide the render.")


# Creates and returns a panel for the mask layer for the given index
def create_mask_panel(index):
    class MaskPanel(PlaybookPanel, bpy.types.Panel):
        bl_idname = f"SCENE_PT_maskpanel{index}"
        bl_label = f"Mask {index + 1}"
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
        column2.label(text="2 credits")

        row1 = box.row()
        row1.scale_y = BUTTON_Y_SCALE
        row1.separator(factor=BOX_PADDING)
        row1.operator("op.queue")
        row1.separator(factor=BOX_PADDING)

        row2 = box.row()
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

        box = layout.box()

        box.separator(factor=BOX_PADDING)

        row1 = box.row()
        row1.scale_y = BUTTON_Y_SCALE
        row1.separator(factor=BOX_PADDING)
        row1.operator("op.send_to_playbook")
        row1.separator(factor=BOX_PADDING)

        row2 = box.row()
        row2.scale_y = BUTTON_Y_SCALE
        row2.separator(factor=BOX_PADDING)
        row2.operator("op.send_to_discord")
        row2.separator(factor=BOX_PADDING)

        box.separator(factor=BOX_PADDING)
