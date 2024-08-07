import bpy
import webbrowser
from .objects import visible_objects
from .render_image import render_image
from bpy.props import StringProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from bpy.app.handlers import persistent


#
class LoginOperator(Operator):
    bl_idname = "op.login"
    bl_label = "skylar@playbookxr.com"

    def execute(self, context):
        return {"FINISHED"}


#
class UpgradeOperator(Operator):
    bl_idname = "op.upgrade"
    bl_label = "Upgrade"

    def execute(self, context):
        return {"FINISHED"}


#
class RandomizePromptOperator(Operator):
    bl_idname = "op.randomize_prompt"
    bl_label = "Randomize"

    def execute(self, context):
        return {"FINISHED"}


#
class RandomizeMaskPromptOperator(Operator):
    bl_idname = "op.randomize_mask_prompt"
    bl_label = "Randomize"

    def execute(self, context):
        return {"FINISHED"}


#
class QueueOperator(Operator):
    bl_idname = "op.queue"
    bl_label = "Open Queue"

    def execute(self, context):
        return {"FINISHED"}


# Render the image according to the settings
class RenderOperator(Operator):
    bl_idname = "op.render_image"
    bl_label = "Render"

    def execute(self, context):
        render_image()
        return {"FINISHED"}


# Direct the user to the Playbook website
class PlaybookWebsiteOperator(Operator):
    bl_idname = "op.send_to_playbook"
    bl_label = ""

    url: StringProperty(name="", default="https://www.playbook3d.com/")

    def execute(self, context):
        webbrowser.open(self.url)
        return {"FINISHED"}


# Direct the user to the Playbook Discord
class PlaybookDiscordOperator(Operator):
    bl_idname = "op.send_to_discord"
    bl_label = ""

    url: StringProperty(name="", default="https://discord.com/invite/FDFEa836Pc")

    def execute(self, context):
        webbrowser.open(self.url)
        return {"FINISHED"}


# Direct the user to the Playbook Twitter
class PlaybookTwitterOperator(Operator):
    bl_idname = "op.send_to_twitter"
    bl_label = ""

    url: StringProperty(name="", default="https://x.com/playbookengine?s=21")

    def execute(self, context):
        webbrowser.open(self.url)
        return {"FINISHED"}


#
class ClearStyleImageOperator(Operator):
    bl_idname = "op.clear_style_image"
    bl_label = ""

    def execute(self, context):
        bpy.context.scene.style_properties.style_image = ""
        return {"FINISHED"}


#
class ClearRelightImageOperator(Operator):
    bl_idname = "op.clear_relight_image"
    bl_label = ""

    def execute(self, context):
        bpy.context.scene.relight_properties.relight_image = ""
        return {"FINISHED"}


classes = [
    LoginOperator,
    UpgradeOperator,
    RandomizePromptOperator,
    RandomizeMaskPromptOperator,
    QueueOperator,
    RenderOperator,
    PlaybookWebsiteOperator,
    PlaybookDiscordOperator,
    PlaybookTwitterOperator,
    ClearStyleImageOperator,
    ClearRelightImageOperator,
]


# Automatically add Mask 1 to the mask list if it is empty
def on_register():
    list = bpy.context.scene.mask_list

    if not list:
        item = list.add()
        item.name = "Mask 1"


def update_object_dropdown():
    update_object_dropdown_handler(bpy.context.scene)


# Set the currently selected object in the viewport as the object dropdown
# option
@persistent
def update_object_dropdown_handler(scene):
    # No mask has been created yet
    if scene.mask_list_index == -1:
        return

    property = getattr(scene, f"mask_properties{scene.mask_list_index + 1}")

    selected_obj = bpy.context.view_layer.objects.active

    if selected_obj and selected_obj.select_get() and selected_obj in visible_objects:
        property.object_dropdown = selected_obj.name

    else:
        property.object_dropdown = "NONE"


def register():
    global classes
    for cls in classes:
        register_class(cls)

    bpy.app.handlers.depsgraph_update_post.append(update_object_dropdown_handler)
    bpy.app.timers.register(update_object_dropdown, first_interval=1)
    bpy.app.timers.register(on_register, first_interval=0.1)


def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)

    bpy.app.handlers.depsgraph_update_post.remove(update_object_dropdown_handler)
