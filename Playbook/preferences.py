import webbrowser
from bpy.types import Operator
from bpy.props import StringProperty
from bpy.utils import register_class, unregister_class
from .properties.workflow_properties import prompt_placeholders
from .version_control import PlaybookVersionControl


class DocumentationOperator(Operator):
    bl_idname = "op.documentation"
    bl_label = "Documentation"
    bl_description = "Open Playbook's documentation in the web browser."

    url: StringProperty(
        name="",
        default="https://playbook3d.notion.site/Blender-Plugin-coming-soon-115471267f0d8068b0fecdbebdbd0ad5",
    )

    def execute(self, context):
        webbrowser.open(self.url)
        return {"FINISHED"}


class UpdateAddonOperator(Operator):
    bl_idname = "op.update_addon"
    bl_label = "Update Addon"

    def execute(self, context):
        PlaybookVersionControl.update_addon()
        return {"FINISHED"}


class ResetAddonOperator(Operator):
    bl_idname = "op.reset_addon_settings"
    bl_label = "Reset Addon"

    def execute(self, context):
        scene = context.scene

        # Global Properties
        scene.global_properties.global_workflow = "RETEXTURE"
        scene.global_properties.global_model = "STABLE"
        scene.global_properties.global_style = "PHOTOREAL"

        # Retexture Properties
        scene.retexture_properties.retexture_prompt = prompt_placeholders["Retexture"]
        scene.retexture_properties.retexture_structure_strength = 50

        # Style Transfer Properties
        scene.style_properties.style_image = ""
        scene.style_properties.style_strength = 50

        # Mask Properties
        scene.mask_list.clear()
        mask = scene.mask_list.add()
        mask.name = "Mask 1"
        scene.mask_list_index = 0

        return {"FINISHED"}


classes = [DocumentationOperator, UpdateAddonOperator, ResetAddonOperator]


def register():
    global classes
    for cls in classes:
        register_class(cls)


def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)
