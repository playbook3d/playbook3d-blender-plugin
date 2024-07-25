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
