import bpy
from .render_status import RenderStatus
from .utilities.utilities import (
    get_filepath,
    download_image,
    load_image_into_blender,
    create_render_filename,
)

filename = ""


#
def open_render_window(image_url: str):
    global filename
    filename = create_render_filename()

    download_image(image_url, get_filepath(filename))

    # Playbook render workspace exists. Set workspace as active
    playbook = bpy.data.workspaces.get("Playbook")
    if playbook:
        bpy.context.window.workspace = playbook
        set_render_area(playbook)
        return

    # Playbook render workspace does not exist. Create a new workspace
    activate_rendering_workspace()

    # Use a timer to delay the duplication to ensure the workspace switch takes effect
    bpy.app.timers.register(get_duplicate_workspace, first_interval=0.1)


#
def activate_rendering_workspace():
    rendering = bpy.data.workspaces.get("Rendering")

    if rendering:
        bpy.context.window.workspace = bpy.data.workspaces[rendering.name]
    else:
        # TODO: What to do if 'Rendering' is not available?
        # For now, use 'Layout' as backup
        layout = bpy.data.workspaces.get("Layout")
        if layout:
            bpy.context.window.workspace = bpy.data.workspaces[layout.name]


#
def get_duplicate_workspace():
    original_name = bpy.context.window.workspace.name

    # Duplicate the current workspace
    bpy.ops.workspace.duplicate()

    new_workspace = bpy.context.window.workspace

    # Rename the workspace
    new_workspace.name = "Playbook"

    set_render_area(new_workspace)

    # Set the workspace name to the original
    bpy.data.workspaces.get(f"{original_name}.001").name = original_name


#
def set_render_area(workspace: bpy.types.WorkSpace):
    global filename

    # Change one of the areas to an Image Editor and set the image to Render Result
    area = get_largest_area(workspace)

    render_image = load_image_into_blender(get_filepath(filename))

    if area.type != "IMAGE_EDITOR":
        area.type = "IMAGE_EDITOR"

    for space in area.spaces:
        if space.type == "IMAGE_EDITOR":
            space.image = render_image
            break

    # Set the new workspace as active
    bpy.context.window.workspace = workspace

    RenderStatus.is_rendering = False


#
def get_largest_area(workspace: bpy.types.WorkSpace) -> bpy.types.Area:
    largest_area = None
    max_size = 0

    # Iterate through all screens in the workspace
    for screen in workspace.screens:
        # Iterate through all areas in the screen
        for area in screen.areas:
            # Calculate the size of the area (width * height)
            area_size = area.width * area.height

            # Check if this area is larger than the current largest
            if area_size > max_size:
                max_size = area_size
                largest_area = area

    return largest_area
