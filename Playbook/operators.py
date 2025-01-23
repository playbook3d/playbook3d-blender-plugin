import bpy
import webbrowser
from .objects.objects import mask_objects
from .capture_passes import capture_passes
from .properties.user_properties import update_user_properties
from .run_workflow import run_single_image_capture
from .sequence_capture import start_sequence_capture, end_sequence_capture
from .utilities.network_utilities import get_user_info
from bpy.props import StringProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from bpy.app.handlers import persistent


#
class LoginOperator(Operator):
    bl_idname = "op.login"
    bl_label = "Enter API Key In Preferences"
    bl_description = "Open up the preferences panel to Playbook."

    def execute(self, context):
        bpy.ops.screen.userpref_show("INVOKE_DEFAULT")
        bpy.context.preferences.active_section = "ADDONS"
        bpy.ops.preferences.addon_expand(module=__package__)
        bpy.ops.preferences.addon_show(module=__package__)

        return {"FINISHED"}


#
class RefreshUserOperator(Operator):
    bl_idname = "op.refresh"
    bl_label = "Refresh"
    bl_description = "Refresh your teams and workflows."

    def execute(self, context):
        user_info = get_user_info()

        if user_info is not None:
            update_user_properties(
                user_info["email"], user_info["teams"], user_info["workflows"]
            )
            return {"FINISHED"}

        return {"CANCELLED"}


#
class DashboardOperator(Operator):
    bl_idname = "op.dashboard"
    bl_label = "Open Dashboard"
    bl_description = "Open the Playbook dashboard"

    url: StringProperty(name="", default="https://www.beta.playbook3d.com/")

    def execute(self, context):
        webbrowser.open(self.url)
        return {"FINISHED"}


#
class CapturePassesOperator(Operator):
    bl_idname = "op.capture_passes"
    bl_label = "Capture Passes"
    bl_description = "Capture passes"

    def execute(self, context):
        capture_passes(True)
        return {"FINISHED"}


#
class SingleImageCaptureOperator(Operator):
    bl_idname = "op.single_image_capture"
    bl_label = "Single Image Capture"
    bl_description = "Single image capture"

    def execute(self, context):
        run_single_image_capture()
        return {"FINISHED"}


#
class StartSequenceCaptureOperator(Operator):
    bl_idname = "op.start_sequence_capture"
    bl_label = "Start Sequence Capture"
    bl_description = "Start sequence capture"

    @classmethod
    def poll(cls, context):
        return not context.scene.render_properties.is_capturing_sequence

    def execute(self, context):
        start_sequence_capture()
        return {"FINISHED"}


#
class EndSequenceCaptureOperator(Operator):
    bl_idname = "op.end_sequence_capture"
    bl_label = "End Sequence Capture"
    bl_description = "End sequence capture"

    @classmethod
    def poll(cls, context):
        return context.scene.render_properties.is_capturing_sequence

    def execute(self, context):
        end_sequence_capture()
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


classes = [
    LoginOperator,
    RefreshUserOperator,
    DashboardOperator,
    CapturePassesOperator,
    SingleImageCaptureOperator,
    StartSequenceCaptureOperator,
    EndSequenceCaptureOperator,
    PlaybookWebsiteOperator,
    PlaybookDiscordOperator,
    PlaybookTwitterOperator,
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
    if not hasattr(scene, "mask_list_index"):
        return

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
