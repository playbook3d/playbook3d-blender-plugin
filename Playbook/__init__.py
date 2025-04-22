bl_info = {
    "name": "Playbook",
    "description": "Playbook is a generative media platform for teams & studios.",
    "author": "Playbook",
    "location": "Properties > Render > Playbook",
    "version": (1, 1, 2),
    "blender": (4, 2, 0),
    "category": "Render",
}

import bpy
import os
import toml
from bpy.types import AddonPreferences
from bpy.props import StringProperty
from bpy.app.handlers import persistent

# --- Playbook modules ---
from . import ui
from . import properties
from . import operators
from . import preferences
from . import task_queue
from .version_control import PlaybookVersionControl
from .utilities.secret_manager import BlenderSecretsManager
from .utilities.network_utilities import get_user_info
from .properties.user_properties import update_user_properties
from .objects.objects import mask_objects  # <-- mask_objects to clear on load


def reset_addon_values():
    from .render_status import RenderStatus
    RenderStatus.is_rendering = False


reset_addon_values()


class Preferences(AddonPreferences):
    bl_idname = __package__

    def on_api_key_updated(self, context):
        if not self.api_key or len(self.api_key) != 36:
            return

        user_info = get_user_info()
        if user_info is not None:
            update_user_properties(
                user_info["email"], user_info["teams"], user_info["workflows"]
            )

    api_key: StringProperty(
        name="API Key",
        default="",
        description="Your Playbook API key",
        update=lambda self, context: self.on_api_key_updated(context),
        options={"TEXTEDIT_UPDATE"},
    )

    def draw(self, context):
        layout = self.layout

        if PlaybookVersionControl.can_update:
            layout.alert = True
            layout.label(text=PlaybookVersionControl.version_control_label)
            layout.alert = False
            layout.operator("op.update_addon")
        else:
            layout.label(text=PlaybookVersionControl.version_control_label)

        layout.operator("op.documentation")
        layout.prop(self, "api_key")


@persistent
def read_preferences_on_load(dummy):
    addon_prefs = bpy.context.preferences.addons[__package__].preferences

    if not addon_prefs.api_key or len(addon_prefs.api_key) != 36:
        return

    user_info = get_user_info()
    if user_info is not None:
        update_user_properties(
            user_info["email"], user_info["teams"], user_info["workflows"]
        )

@persistent
def clear_masks_on_load(dummy):
    scene = bpy.context.scene
    print("🔁 Scene loaded — running clear_masks_on_load")

    # 1. Clear runtime mask mappings
    for key in mask_objects:
        mask_objects[key].clear()

    # 2. Clear UI-facing list
    if hasattr(scene, "mask_list"):
        scene.mask_list.clear()
        scene.mask_list_index = 0

    # 3. Clear mask_data.masks[i].objects
    if hasattr(scene, "mask_data") and hasattr(scene.mask_data, "masks"):
        for i, mask in enumerate(scene.mask_data.masks):
            if hasattr(mask, "objects"):
                mask.objects.clear()

    # 4. Clear mask_properties1-3.mask_objects (actual visible list in UI)
    for i in range(1, 4):  # Adjust if NUM_MASKS_ALLOWED is different
        prop_name = f"mask_properties{i}"
        if hasattr(scene, prop_name):
            mask_prop = getattr(scene, prop_name)
            if hasattr(mask_prop, "mask_objects"):
                mask_prop.mask_objects.clear()
                print(f"🧹 Cleared mask_objects in {prop_name}")

    # 5. Redraw UI
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type in {'PROPERTIES', 'VIEW_3D'}:
                area.tag_redraw()

    print("✅ All masks, UI lists, and runtime mappings cleared.")


def register():
    properties.register()
    ui.register()
    operators.register()
    preferences.register()
    task_queue.register()

    bpy.utils.register_class(Preferences)
    BlenderSecretsManager.load_to_env()

    # Version check
    toml_path = os.path.join(os.path.dirname(__file__), "blender_manifest.toml")
    with open(toml_path, "r") as blender_info:
        version = toml.load(blender_info)["version"]
        PlaybookVersionControl.check_if_version_up_to_date(
            tuple(map(int, version.split(".")))
        )

    # Persistent handlers
    if read_preferences_on_load not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(read_preferences_on_load)

    if clear_masks_on_load not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(clear_masks_on_load)


def unregister():
    if read_preferences_on_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(read_preferences_on_load)

    if clear_masks_on_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(clear_masks_on_load)

    try:
        properties.unregister()
        ui.unregister()
        operators.unregister()
        preferences.unregister()
        task_queue.unregister()

        bpy.utils.unregister_class(Preferences)
        reset_addon_values()

    except Exception as e:
        print("❌ Unregister error:", e)