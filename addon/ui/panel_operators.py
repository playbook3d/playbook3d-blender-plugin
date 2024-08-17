import bpy
from bpy.types import Operator
from bpy.utils import register_class, unregister_class


# Operator to show / hide the 'Global' panel
class RetexturePanelOperator(Operator):
    bl_idname = "op.retexture_panel"
    bl_label = "Retexture"
    bl_description = "Retexture"

    def execute(self, context):

        return {"FINISHED"}


# Operator to show / hide the 'Style Transfer' panel
class StylePanelOperator(Operator):
    bl_idname = "op.style_panel"
    bl_label = "Style Transfer"
    bl_description = "Style transfer"

    def execute(self, context):
        bpy.context.scene.show_style_panel = not bpy.context.scene.show_style_panel
        return {"FINISHED"}


# Operator to show / hide the 'Relight' panel
class RelightPanelOperator(Operator):
    bl_idname = "op.relight_panel"
    bl_label = "Relight"
    bl_description = "Relight"

    def execute(self, context):
        bpy.context.scene.show_relight_panel = not bpy.context.scene.show_relight_panel
        return {"FINISHED"}


# Operator to show / hide the 'Upscale' panel
class UpscalePanelOperator(Operator):
    bl_idname = "op.upscale_panel"
    bl_label = "Upscale"
    bl_description = "Upscale"

    def execute(self, context):
        bpy.context.scene.show_upscale_panel = not bpy.context.scene.show_upscale_panel
        return {"FINISHED"}


classes = []


def register():
    global classes
    for cls in classes:
        register_class(cls)


def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)
