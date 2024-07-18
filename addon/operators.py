import bpy
from .render_image import render_image


class RenderOperator(bpy.types.Operator):
    bl_idname = "object.render_image"
    bl_label = "Render"

    def execute(self, context):
        render_image(context)
        return {"FINISHED"}
