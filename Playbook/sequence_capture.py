import bpy
from .render_passes.render_passes import render_passes
from .utilities.file_utilities import clear_render_folder, create_zip_destination_folder


frames_per_second = 24
max_frames = 120
time_interval = 0


def start_sequence_capture():
    """
    Reset the relevant properties and begin capturing sequences
    based off the given frames per second
    """

    print("Starting sequence capture")

    bpy.context.scene.render_properties.is_capturing_sequence = True
    bpy.context.scene.render_properties.capture_count = 0
    time_interval = 1 / frames_per_second

    clear_render_folder()

    create_zip_destination_folder("renders", "beauty_zip")
    create_zip_destination_folder("renders", "mask_zip")

    bpy.app.timers.register(render_sequence_pass, first_interval=time_interval)


#
def end_sequence_capture():
    """
    End capturing sequences and begin the run workflow process
    """

    print("Ending sequence capture")

    bpy.context.scene.render_properties.is_capturing_sequence = False

    # TODO: Add logic to zip captures


#
def render_sequence_pass():
    properties = bpy.context.scene.render_properties

    # End sequence capture
    if not properties.is_capturing_sequence:
        return None

    properties.capture_count += 1

    # TODO: Render passes to file
    render_passes(False)

    # At maximum capture count
    if properties.capture_count >= max_frames:
        return None

    # Continue capturing
    return time_interval


#
def zip_renders():
    return


#
def send_zips_to_urls():
    return
