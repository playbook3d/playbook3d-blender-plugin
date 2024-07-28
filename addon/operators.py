import bpy
import webbrowser
from .render_image import render_image
from bpy.props import StringProperty
from bpy.types import Operator


#
class LoginOperator(Operator):
    bl_idname = "op.login"
    bl_label = "skylar@playbookxr.com"

    def execute(self, context):
        return {"FINISHED"}


#
class CreditsOperator(Operator):
    bl_idname = "op.credits"
    bl_label = "Get Credits"

    def execute(self, context):
        return {"FINISHED"}


#
class GeneralPanelOperator(Operator):
    bl_idname = "op.general_panel"
    bl_label = "Global"

    def execute(self, context):
        bpy.context.scene.show_general_panel = not bpy.context.scene.show_general_panel
        return {"FINISHED"}


#
class RandomizePromptOperator(Operator):
    bl_idname = "op.randomize_prompt"
    bl_label = "Randomize"

    def execute(self, context):
        return {"FINISHED"}


#
class ObjectMaskPanelOperator(Operator):
    bl_idname = "op.object_mask_panel"
    bl_label = "Object Mask"

    def execute(self, context):
        bpy.context.scene.show_mask_panel = not bpy.context.scene.show_mask_panel
        return {"FINISHED"}


#
class StylePanelOperator(Operator):
    bl_idname = "op.style_panel"
    bl_label = "Style Transfer"

    def execute(self, context):
        bpy.context.scene.show_style_panel = not bpy.context.scene.show_style_panel
        return {"FINISHED"}


#
class RelightPanelOperator(Operator):
    bl_idname = "op.relight_panel"
    bl_label = "Relight"

    def execute(self, context):
        bpy.context.scene.show_relight_panel = not bpy.context.scene.show_relight_panel
        return {"FINISHED"}


#
class UpscalePanelOperator(Operator):
    bl_idname = "op.upscale_panel"
    bl_label = "Upscale"

    def execute(self, context):
        bpy.context.scene.show_upscale_panel = not bpy.context.scene.show_upscale_panel
        return {"FINISHED"}


#
class MaskPropertyPanelOperator1(Operator):
    bl_idname = "op.mask_property_panel1"
    bl_label = "Mask 1"
    property_name = "show_mask_properties1"

    def execute(self, context):
        # Toggle the property
        current_value = getattr(context.scene, self.property_name)
        setattr(context.scene, self.property_name, not current_value)
        return {"FINISHED"}


#
class MaskPropertyPanelOperator2(Operator):
    bl_idname = "op.mask_property_panel2"
    bl_label = "Mask 2"
    property_name = "show_mask_properties2"

    def execute(self, context):
        # Toggle the property
        current_value = getattr(context.scene, self.property_name)
        setattr(context.scene, self.property_name, not current_value)
        return {"FINISHED"}


#
class MaskPropertyPanelOperator3(Operator):
    bl_idname = "op.mask_property_panel3"
    bl_label = "Mask 3"
    property_name = "show_mask_properties3"

    def execute(self, context):
        # Toggle the property
        current_value = getattr(context.scene, self.property_name)
        setattr(context.scene, self.property_name, not current_value)
        return {"FINISHED"}


#
class MaskPropertyPanelOperator4(Operator):
    bl_idname = "op.mask_property_panel4"
    bl_label = "Mask 4"
    property_name = "show_mask_properties4"

    def execute(self, context):
        # Toggle the property
        current_value = getattr(context.scene, self.property_name)
        setattr(context.scene, self.property_name, not current_value)
        return {"FINISHED"}


#
class MaskPropertyPanelOperator5(Operator):
    bl_idname = "op.mask_property_panel5"
    bl_label = "Mask 5"
    property_name = "show_mask_properties5"

    def execute(self, context):
        # Toggle the property
        current_value = getattr(context.scene, self.property_name)
        setattr(context.scene, self.property_name, not current_value)
        return {"FINISHED"}


#
class MaskPropertyPanelOperator6(Operator):
    bl_idname = "op.mask_property_panel6"
    bl_label = "Mask 6"
    property_name = "show_mask_properties6"

    def execute(self, context):
        # Toggle the property
        current_value = getattr(context.scene, self.property_name)
        setattr(context.scene, self.property_name, not current_value)
        return {"FINISHED"}


#
class MaskPropertyPanelOperator7(Operator):
    bl_idname = "op.mask_property_panel7"
    bl_label = "Mask 7"
    property_name = "show_mask_properties7"

    def execute(self, context):
        # Toggle the property
        current_value = getattr(context.scene, self.property_name)
        setattr(context.scene, self.property_name, not current_value)
        return {"FINISHED"}


#
class QueueOperator(Operator):
    bl_idname = "op.queue"
    bl_label = "Open Queue"

    def execute(self, context):
        return {"FINISHED"}


#
class RenderOperator(Operator):
    bl_idname = "op.render_image"
    bl_label = "Render"

    def execute(self, context):
        render_image()
        return {"FINISHED"}


#
class PlaybookWebsiteOperator(Operator):
    bl_idname = "op.send_to_playbook"
    bl_label = ""

    url: StringProperty(name="", default="https://www.playbookengine.com/")

    def execute(self, context):
        webbrowser.open(self.url)
        return {"FINISHED"}


#
class PlaybookDiscordOperator(Operator):
    bl_idname = "op.send_to_discord"
    bl_label = ""

    url: StringProperty(name="", default="https://discord.com/invite/FDFEa836Pc")

    def execute(self, context):
        webbrowser.open(self.url)
        return {"FINISHED"}


#
class PlaybookTwitterOperator(Operator):
    bl_idname = "op.send_to_twitter"
    bl_label = ""

    url: StringProperty(name="", default="https://x.com/playbookengine?s=21")

    def execute(self, context):
        webbrowser.open(self.url)
        return {"FINISHED"}


#
class MaskListAddItem(Operator):
    bl_idname = "list.add_mask_item"
    bl_label = ""

    def execute(self, context):
        item = context.scene.mask_list.add()
        item.name = f"Mask {len(context.scene.mask_list)}"
        return {"FINISHED"}


#
class MaskListRemoveItem(Operator):
    bl_idname = "list.remove_mask_item"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return context.scene.mask_list

    def execute(self, context):
        mask_list = context.scene.mask_list
        index = len(context.scene.mask_list) - 1

        mask_list.remove(index)

        if index == context.scene.mask_list_index:
            context.scene.mask_list_index = min(max(0, index - 1), len(mask_list) - 1)

        return {"FINISHED"}


#
class MaskObjectListAddItem(Operator):
    bl_idname = "list.add_mask_object_item"
    bl_label = ""

    def execute(self, context):
        obj = bpy.context.active_object
        if not obj or obj.type != "MESH":
            return {"CANCELLED"}

        mask_index = context.scene.mask_list_index
        mask = getattr(context.scene, f"mask_properties{mask_index + 1}")

        for item in mask.mask_objects:
            if item.object_id == obj.name_full:
                return {"CANCELLED"}

        item = mask.mask_objects.add()
        item.name = obj.name
        item.object_id = obj.name_full

        for item in mask.mask_objects:
            print(item.object_id)

        return {"FINISHED"}
