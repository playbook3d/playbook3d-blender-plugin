import bpy
import webbrowser
import functools
from .objects.objects import mask_objects
from .capture_passes import capture_passes
from .run_workflow import run_workflow
from .task_queue import add
from bpy.props import StringProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from bpy.app.handlers import persistent


#
class LoginOperator(Operator):
    bl_idname = "op.login"
    bl_label = "Enter API key in Preferences"
    bl_description = "Open up the preferences panel to Playbook."

    def execute(self, context):
        bpy.ops.screen.userpref_show("INVOKE_DEFAULT")
        bpy.context.preferences.active_section = "ADDONS"
        bpy.ops.preferences.addon_expand(module=__package__)
        bpy.ops.preferences.addon_show(module=__package__)

        return {"FINISHED"}


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
        add(functools.partial(capture_passes))
        return {"FINISHED"}


#
class RunWorkflowOperator(Operator):
    bl_idname = "op.run_workflow"
    bl_label = "Run Workflow"
    bl_description = "Run workflow"

    def execute(self, context):
        add(functools.partial(run_workflow))
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
    DashboardOperator,
    CapturePassesOperator,
    RunWorkflowOperator,
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
