import bpy
from .utilities.file_utilities import clear_render_folder


class SequenceCapture:
    is_capturing = False
    frames_per_second = 24
    max_frames = 120
    time_interval = 0
    capture_count = 0

    def start_sequence_capture(self):
        """
        Reset the relevant properties and begin capturing sequences
        based off the given frames per second
        """

        self.is_capturing = True
        self.time_interval = 1 / self.frames_per_second
        self.capture_count = 0

        bpy.app.timers.register(self.render_passes, first_interval=self.time_interval)

    #
    def end_sequence_capture(self):
        """
        End capturing sequences and begin the run workflow process
        """

        self.is_capturing = False

        # TODO: Add logic to zip captures

    #
    def render_passes(self):
        # End sequence capture
        if not self.is_capturing:
            return None

        self.capture_count += 1

        # TODO: Render passes to file

        # At maximum capture count
        if self.capture_count >= self.max_frames:
            return None

        # Continue capturing
        return self.time_interval

    #
    def zip_renders(self):
        return

    #
    def send_zips_to_urls(self):
        return
