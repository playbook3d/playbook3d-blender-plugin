import bpy
import webbrowser
from .render_image import render_image
from .properties import mask_objects
from bpy.props import StringProperty
from bpy.types import Operator


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


# Operator to show / hide the 'General' panel
class RetexturePanelOperator(Operator):
    bl_idname = "op.retexture_panel"
    bl_label = "Retexture"

    def execute(self, context):
        bpy.context.scene.show_retexture_panel = (
            not bpy.context.scene.show_retexture_panel
        )
        return {"FINISHED"}


#
class RandomizePromptOperator(Operator):
    bl_idname = "op.randomize_prompt"
    bl_label = "Randomize"

    def execute(self, context):
        return {"FINISHED"}


# Operator to show / hide the 'Object Masks' panel
class ObjectMaskPanelOperator(Operator):
    bl_idname = "op.object_mask_panel"
    bl_label = "Object Mask"

    def execute(self, context):
        bpy.context.scene.show_mask_panel = not bpy.context.scene.show_mask_panel
        return {"FINISHED"}


# Operator to show / hide the 'Style Transfer' panel
class StylePanelOperator(Operator):
    bl_idname = "op.style_panel"
    bl_label = "Style Transfer"

    def execute(self, context):
        bpy.context.scene.show_style_panel = not bpy.context.scene.show_style_panel
        return {"FINISHED"}


# Operator to show / hide the 'Relight' panel
class RelightPanelOperator(Operator):
    bl_idname = "op.relight_panel"
    bl_label = "Relight"

    def execute(self, context):
        bpy.context.scene.show_relight_panel = not bpy.context.scene.show_relight_panel
        return {"FINISHED"}


# Operator to show / hide the 'Upscale' panel
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

    url: StringProperty(name="", default="https://www.playbookengine.com/")

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


# Add a mask to the mask list
class MaskListAddItem(Operator):
    bl_idname = "list.add_mask_item"
    bl_label = ""

    def execute(self, context):
        mask_len = len(context.scene.mask_list)

        if mask_len == 7:
            return {"CANCELLED"}

        item = context.scene.mask_list.add()
        item.name = f"Mask {mask_len + 1}"

        context.scene.mask_list_index = len(context.scene.mask_list) - 1

        return {"FINISHED"}


# Remove the last mask from the mask list
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

        if len(mask_list) > 0:
            context.scene.mask_list_index = 0
        else:
            context.scene.mask_list_index = -1

        return {"FINISHED"}


# Add the currently selected object (in the viewport) to the
# currently selected mask
class MaskObjectListAddItem(Operator):
    bl_idname = "list.add_mask_object_item"
    bl_label = ""

    def execute(self, context):
        obj = bpy.context.active_object

        # There is no currently selected object or the currently
        # selected object is not a mesh
        if not obj or obj.type != "MESH":
            return {"CANCELLED"}

        mask_index = context.scene.mask_list_index
        mask = getattr(context.scene, f"mask_properties{mask_index + 1}")

        # The currently selected item is already part of the list
        for item in mask.mask_objects:
            if item.object_id == obj.name_full:
                return {"CANCELLED"}

        item = mask.mask_objects.add()
        item.name = obj.name
        item.object_id = obj.name_full

        mask_objects[f"MASK{mask_index + 1}"].append(item.object_id)

        print("ADDED")
        for item in mask.mask_objects:
            print(item.name)
            print(item.object_id)

        return {"FINISHED"}


# Remove the currently selected index in the list from the
# currently selected mask
class MaskObjectListRemoveItem(Operator):
    bl_idname = "list.remove_mask_object_item"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        mask_index = context.scene.mask_list_index
        return getattr(context.scene, f"mask_properties{mask_index + 1}")

    def execute(self, context):
        mask_index = context.scene.mask_list_index
        mask = getattr(context.scene, f"mask_properties{mask_index + 1}")

        if len(mask.mask_objects) == 0:
            return {"CANCELLED"}

        index = mask.object_list_index

        # No object list index is selected but items exists in the list
        # Delete the last object
        if index == -1 and len(mask.mask_objects) > 0:
            index = len(mask.mask_objects) - 1

        mask.mask_objects.remove(index)
        mask_objects[f"MASK{mask_index + 1}"].pop(index)

        if len(mask.mask_objects) > 0:
            mask.object_list_index = 0
        else:
            mask.object_list_index = -1

        return {"FINISHED"}


# Clear all the objects from the currently selected mask
class MaskObjectListClearItems(Operator):
    bl_idname = "list.clear_mask_object_list"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        mask_index = context.scene.mask_list_index
        return getattr(context.scene, f"mask_properties{mask_index + 1}")

    def execute(self, context):
        mask_index = context.scene.mask_list_index
        mask = getattr(context.scene, f"mask_properties{mask_index + 1}")

        mask.mask_objects.clear()

        mask.object_list_index = -1

        return {"FINISHED"}
