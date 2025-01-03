import bpy
from .upload_files import upload_single_frame_files
from .render_passes.render_passes import render_passes
from .utilities.file_utilities import clear_render_folder


def capture_passes():
    clear_render_folder()

    render_passes(True)

    upload_single_frame_files()

    return


# Returns True if an error occurs while attempting to render the image.
def error_exists_in_capture_passes(scene) -> bool:
    # [workflow, condition for error message]
    workflow_checks = {
        "APIKEY": bpy.context.preferences.addons.get("Playbook").preferences.api_key
        == "",
    }

    # [workflow, error message]
    messages = {
        "APIKEY": "Copy your API key from the Playbook web editor.",
    }

    for key, val in workflow_checks.items():
        if val:
            scene.error_message = messages[key]
            return True

    scene.error_message = ""
    return False
