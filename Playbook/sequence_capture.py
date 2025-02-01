import bpy
from .render_passes.render_passes import render_passes
from .run_workflow import run_workflow
from .upload_files import upload_sequence_capture_files
from .utilities.network_utilities import get_run_id
from .utilities.utilities import does_plugin_error_exists
from .utilities.file_utilities import (
    clear_folder_contents,
    create_folder,
    zip_folder,
    get_filepath,
)


frames_per_second = 24
max_frames = 120
time_interval = 0


def start_sequence_capture():
    """
    Reset the relevant properties and begin capturing sequences
    based off the given frames per second
    """

    if does_plugin_error_exists():
        return

    print("Starting sequence capture")

    bpy.context.scene.render_properties.is_capturing_sequence = True
    bpy.context.scene.render_properties.capture_count = 0
    time_interval = 1 / frames_per_second

    clear_folder_contents("renders")

    create_folder("renders", "beauty_zip")
    create_folder("renders", "mask_zip")

    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = max_frames
    bpy.context.scene.frame_current = 1

    bpy.ops.screen.animation_play()

    bpy.app.timers.register(render_sequence_pass, first_interval=time_interval)


#
def end_sequence_capture():
    """
    End capturing sequences and begin the run workflow process
    """

    print("Ending sequence capture")

    bpy.ops.screen.animation_cancel(restore_frame=True)

    bpy.context.scene.render_properties.is_capturing_sequence = False

    # Zip sequence capture folders
    beauty_folder = get_filepath("renders/beauty_zip")
    mask_folder = get_filepath("renders/mask_zip")
    zip_folder(beauty_folder)
    zip_folder(mask_folder)

    run_id = get_run_id()

    # Send zips to server
    upload_sequence_capture_files(run_id)

    run_workflow(run_id)


#
def render_sequence_pass():
    properties = bpy.context.scene.render_properties

    # End sequence capture
    if not properties.is_capturing_sequence:
        return None

    properties.capture_count += 1

    # Render passes to file
    render_passes(False)

    # At maximum capture count
    if properties.capture_count >= max_frames:
        end_sequence_capture()
        return None

    # Continue capturing
    return time_interval
