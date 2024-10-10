from .utilities.utilities import force_ui_redraw


class RenderStatus:
    is_rendering = False
    render_status = ""

    @classmethod
    def set_render_status(cls, status: str):
        print(status)

        if status == "not-started":
            cls.render_status = "Not started"
        elif status in {"queued", "running", "started"}:
            cls.render_status = status.capitalize()
        else:
            cls.render_status = status

        force_ui_redraw()
