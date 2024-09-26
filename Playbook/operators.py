import bpy
import webbrowser
from .objects import mask_objects
from .render_image import render_image
from .comfy_deploy_api.network import ComfyDeployClient
from .properties import prompt_placeholders
from bpy.props import StringProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from bpy.app.handlers import persistent


class ResetAddonOperator(Operator):
    bl_idname = "op.reset_addon_settings"
    bl_label = "Reset Addon"

    def execute(self, context):
        print("Resetting")

        scene = context.scene

        # Global Properties
        scene.global_properties.global_workflow = "RETEXTURE"
        scene.global_properties.global_model = "STABLE"
        scene.global_properties.global_style = "PHOTOREAL"

        # Retexture Properties
        scene.retexture_properties.retexture_prompt = prompt_placeholders["Retexture"]
        scene.retexture_properties.retexture_structure_strength = 50

        # Style Transfer Properties
        scene.style_properties.style_image = None
        scene.style_properties.style_strength = 50

        # Mask Properties
        scene.mask_list.clear()
        mask = scene.mask_list.add()
        mask.name = "Mask 1"
        scene.mask_list_index = 0

        return {"FINISHED"}


#
class LoginOperator(Operator):
    bl_idname = "op.login"
    bl_label = "Logged in as Skylar"
    bl_description = "Logged in"

    def execute(self, context):
        return {"FINISHED"}


#
class UpgradeOperator(Operator):
    bl_idname = "op.upgrade"
    bl_label = "Get Credits"
    bl_description = "Upgrade"

    def execute(self, context):
        return {"FINISHED"}


#
class RandomizePromptOperator(Operator):
    bl_idname = "op.randomize_prompt"
    bl_label = "Randomize"
    bl_description = "Randomize"

    def execute(self, context):
        return {"FINISHED"}


#
class RandomizeMaskPromptOperator(Operator):
    bl_idname = "op.randomize_mask_prompt"
    bl_label = "Randomize"
    bl_description = "Randomize"

    def execute(self, context):
        return {"FINISHED"}


#
class QueueOperator(Operator):
    bl_idname = "op.queue"
    bl_label = "Open Queue"
    bl_description = "Open queue"

    url: StringProperty(name="", default="https://www.beta.playbook3d.com/")

    def execute(self, context):
        webbrowser.open(self.url)
        return {"FINISHED"}


# Render the image according to the settings
class RenderOperator(Operator):
    bl_idname = "op.render_image"
    bl_label = "Render"
    bl_description = "Render the image"

    @classmethod
    def poll(cls, context):
        return not context.scene.is_rendering

    def execute(self, context):
        render_image()
        return {"FINISHED"}


# Direct the user to the Playbook website
class PlaybookWebsiteOperator(Operator):
    bl_idname = "op.send_to_playbook"
    bl_label = ""
    bl_description = "Go to Playbook3D"

    url: StringProperty(name="", default="https://www.playbook3d.com/")

    def execute(self, context):
        webbrowser.open(self.url)
        return {"FINISHED"}


# Direct the user to the Playbook Discord
class PlaybookDiscordOperator(Operator):
    bl_idname = "op.send_to_discord"
    bl_label = ""
    bl_description = "Join our Discord"

    url: StringProperty(name="", default="https://discord.com/invite/FDFEa836Pc")

    def execute(self, context):
        webbrowser.open(self.url)
        return {"FINISHED"}


# Direct the user to the Playbook Twitter
class PlaybookTwitterOperator(Operator):
    bl_idname = "op.send_to_twitter"
    bl_label = ""
    bl_description = "Check out our Twitter"

    url: StringProperty(name="", default="https://x.com/playbook3d")

    def execute(self, context):
        webbrowser.open(self.url)
        return {"FINISHED"}


#
class ClearStyleTransferImageOperator(Operator):
    bl_idname = "op.clear_style_transfer_image"
    bl_label = ""
    bl_description = "Clear the file"

    @classmethod
    def poll(cls, context):
        return context.scene.style_properties.style_image

    def execute(self, context):
        context.scene.style_properties.style_image = ""
        return {"FINISHED"}


#
class ClearRelightImageOperator(Operator):
    bl_idname = "op.clear_relight_image"
    bl_label = ""
    bl_description = "Choose an image from local files"

    def execute(self, context):
        context.scene.relight_properties.relight_image = ""
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
    ClearStyleTransferImageOperator,
    ClearRelightImageOperator,
    ResetAddonOperator,
]


# Automatically add Mask 1 to the mask list if it is empty
def on_register():
    list = bpy.context.scene.mask_list

    if not list:
        item = list.add()
        item.name = "Mask 1"


previous_objects = {}


#
def update_object_dropdown():
    update_object_dropdown_handler(bpy.context.scene)


# Set the currently selected object in the viewport as the object
# dropdown option
@persistent
def update_object_dropdown_handler(scene):
    # No mask exists
    if scene.mask_list_index == -1:
        return

    selected_objects = [obj.name for obj in bpy.context.selected_objects]

    if selected_objects:
        scene.show_object_dropdown = False
    else:
        scene.show_object_dropdown = True


@persistent
def check_for_deleted_objects_handler(scene):
    global previous_objects

    if not previous_objects:
        previous_objects = set(scene.objects.keys())
        return

    # Compare current objects to previous objects. If current objects has objects
    # missing from previous objects, they were deleted
    current_objects = set(scene.objects.keys())
    deleted_objects = previous_objects - current_objects

    # An object(s) was deleted
    if deleted_objects:
        for del_obj in deleted_objects:
            for key, value in mask_objects.items():
                # Object is part of the mask. Delete from mask
                if del_obj in value:
                    remove_object_from_list(scene, key, del_obj)

        # Update mask dropdown
        obj = bpy.context.active_object
        # There is no selected object. Reset dropdown to None
        if not obj or not obj.select_get():
            mask_index = scene.mask_list_index
            mask = getattr(scene, f"mask_properties{mask_index + 1}")
            mask.object_dropdown = "NONE"

    previous_objects = current_objects


# Remove the given objects from the mask lists
def remove_object_from_list(scene, mask: str, obj_name: str):
    mask_index = mask[-1]
    mask_props = getattr(scene, f"mask_properties{mask_index}")

    obj_index = mask_objects[mask].index(obj_name)

    mask_props.mask_objects.remove(obj_index)
    mask_objects[mask].pop(obj_index)

    mask_props.object_list_index = 0 if mask_props.mask_objects else -1


def register():
    global classes
    for cls in classes:
        register_class(cls)

    bpy.app.handlers.depsgraph_update_post.append(update_object_dropdown_handler)
    bpy.app.handlers.depsgraph_update_post.append(check_for_deleted_objects_handler)
    bpy.app.timers.register(update_object_dropdown, first_interval=1)
    bpy.app.timers.register(on_register, first_interval=0.1)


def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)

    bpy.app.handlers.depsgraph_update_post.remove(update_object_dropdown_handler)
    bpy.app.handlers.depsgraph_update_post.remove(check_for_deleted_objects_handler)
