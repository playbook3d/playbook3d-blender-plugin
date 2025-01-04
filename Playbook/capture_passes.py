from .upload_files import upload_single_capture_files
from .render_passes.render_passes import render_passes
from .utilities.file_utilities import clear_folder_contents
from .utilities.utilities import does_plugin_error_exists


def capture_passes():
    """
    Render and upload the selected single image capture passes.
    """

    if does_plugin_error_exists():
        return

    clear_folder_contents("renders")

    render_passes(is_image=True)

    upload_single_capture_files()
