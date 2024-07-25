import bpy
import webbrowser
from .render_image import render_image
from bpy.props import StringProperty


#
class LoginOperator(bpy.types.Operator):
    bl_idname = "op.login"
    bl_label = "skylar@playbookxr.com"

    def execute(self, context):
        return {"FINISHED"}


#
class CreditsOperator(bpy.types.Operator):
    bl_idname = "op.credits"
    bl_label = "100 credits remaining"

    def execute(self, context):
        return {"FINISHED"}


#
class GlobalPanelOperator(bpy.types.Operator):
    bl_idname = "op.global_panel"
    bl_label = "Global"

    def execute(self, context):
        bpy.context.scene.show_global_panel = not bpy.context.scene.show_global_panel
        return {"FINISHED"}


#
class ObjectMaskPanelOperator(bpy.types.Operator):
    bl_idname = "op.object_mask_panel"
    bl_label = "Object Mask"

    def execute(self, context):
        bpy.context.scene.show_mask_panel = not bpy.context.scene.show_mask_panel
        return {"FINISHED"}


#
class MaskPropertyPanelOperator1(bpy.types.Operator):
    bl_idname = "op.mask_property_panel1"
    bl_label = "Mask 1"
    property_name = "show_mask_properties1"

    def execute(self, context):
        # Toggle the property
        current_value = getattr(context.scene, self.property_name)
        setattr(context.scene, self.property_name, not current_value)
        return {"FINISHED"}


#
class MaskPropertyPanelOperator2(bpy.types.Operator):
    bl_idname = "op.mask_property_panel2"
    bl_label = "Mask 2"
    property_name = "show_mask_properties2"

    def execute(self, context):
        # Toggle the property
        current_value = getattr(context.scene, self.property_name)
        setattr(context.scene, self.property_name, not current_value)
        return {"FINISHED"}


#
class MaskPropertyPanelOperator3(bpy.types.Operator):
    bl_idname = "op.mask_property_panel3"
    bl_label = "Mask 3"
    property_name = "show_mask_properties3"

    def execute(self, context):
        # Toggle the property
        current_value = getattr(context.scene, self.property_name)
        setattr(context.scene, self.property_name, not current_value)
        return {"FINISHED"}


#
class MaskPropertyPanelOperator4(bpy.types.Operator):
    bl_idname = "op.mask_property_panel4"
    bl_label = "Mask 4"
    property_name = "show_mask_properties4"

    def execute(self, context):
        # Toggle the property
        current_value = getattr(context.scene, self.property_name)
        setattr(context.scene, self.property_name, not current_value)
        return {"FINISHED"}


#
class MaskPropertyPanelOperator5(bpy.types.Operator):
    bl_idname = "op.mask_property_panel5"
    bl_label = "Mask 5"
    property_name = "show_mask_properties5"

    def execute(self, context):
        # Toggle the property
        current_value = getattr(context.scene, self.property_name)
        setattr(context.scene, self.property_name, not current_value)
        return {"FINISHED"}


#
class MaskPropertyPanelOperator6(bpy.types.Operator):
    bl_idname = "op.mask_property_panel6"
    bl_label = "Mask 6"
    property_name = "show_mask_properties6"

    def execute(self, context):
        # Toggle the property
        current_value = getattr(context.scene, self.property_name)
        setattr(context.scene, self.property_name, not current_value)
        return {"FINISHED"}


#
class MaskPropertyPanelOperator7(bpy.types.Operator):
    bl_idname = "op.mask_property_panel7"
    bl_label = "Mask 7"
    property_name = "show_mask_properties7"

    def execute(self, context):
        # Toggle the property
        current_value = getattr(context.scene, self.property_name)
        setattr(context.scene, self.property_name, not current_value)
        return {"FINISHED"}


#
class QueueOperator(bpy.types.Operator):
    bl_idname = "op.queue"
    bl_label = "Open Queue"

    def execute(self, context):
        return {"FINISHED"}


#
class RenderOperator(bpy.types.Operator):
    bl_idname = "op.render_image"
    bl_label = "Render"

    def execute(self, context):
        render_image()
        return {"FINISHED"}


#
class PlaybookWebsiteOperator(bpy.types.Operator):
    bl_idname = "op.send_to_playbook"
    bl_label = "Visit Website"

    url: StringProperty(name="", default="https://www.playbookengine.com/")

    def execute(self, context):
        webbrowser.open(self.url)
        return {"FINISHED"}


#
class PlaybookDiscordOperator(bpy.types.Operator):
    bl_idname = "op.send_to_discord"
    bl_label = "Join Discord"

    url: StringProperty(name="", default="https://discord.com/invite/FDFEa836Pc")

    def execute(self, context):
        webbrowser.open(self.url)
        return {"FINISHED"}
