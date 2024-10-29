import bpy
import os
from ..visible_objects import allowed_obj_types

original_settings = {}

DISTANCE_MARGIN = 4


def calculate_mist_distances():
    camera = bpy.context.scene.camera
    camera_location = camera.location

    closest_distance = float("inf")
    farthest_distance = 0

    # Iterate through all objects in the scene
    for obj in bpy.context.scene.objects:
        if obj.type in allowed_obj_types:
            distance = (obj.location - camera_location).length

            # Check if object is closer than previous closest
            if distance < closest_distance:
                closest_distance = distance

            # Check if object is farther than previous farthest
            if distance > farthest_distance:
                farthest_distance = distance

    if closest_distance != float("inf") and farthest_distance > 0:
        return {"closest": closest_distance, "farthest": farthest_distance}


#
def save_depth_settings():
    global original_settings

    scene = bpy.context.scene

    if not scene.world:
        scene.world = bpy.data.worlds["World"]

    original_settings.clear()
    original_settings.update(
        {
            "use_pass_mist": scene.view_layers["ViewLayer"].use_pass_mist,
            "mist_start": scene.world.mist_settings.start,
            "mist_depth": scene.world.mist_settings.depth,
            "mist_falloff": scene.world.mist_settings.falloff,
            "camera_show_mist": scene.camera.data.show_mist,
        }
    )


#
def set_depth_settings():
    scene = bpy.context.scene

    distances = calculate_mist_distances()
    scene.view_layers["ViewLayer"].use_pass_mist = True
    if distances:
        scene.world.mist_settings.start = distances["closest"] - DISTANCE_MARGIN
        scene.world.mist_settings.depth = (
            distances["farthest"] - distances["closest"] + DISTANCE_MARGIN * 10
        )
    scene.world.mist_settings.falloff = "INVERSE_QUADRATIC"
    scene.camera.data.show_mist = True


#
def reset_depth_settings():
    global original_settings

    scene = bpy.context.scene

    scene.view_layers["ViewLayer"].use_pass_mist = original_settings["use_pass_mist"]
    scene.world.mist_settings.start = original_settings["mist_start"]
    scene.world.mist_settings.depth = original_settings["mist_depth"]
    scene.world.mist_settings.falloff = original_settings["mist_falloff"]
    scene.camera.data.show_mist = original_settings["camera_show_mist"]


#
def render_depth_to_file():
    scene = bpy.context.scene
    render = scene.render

    dir = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(dir, "renders", "render_depth.png")
    render.filepath = output_path

    if scene.node_tree is None:
        scene.use_nodes = True

    node_tree = scene.node_tree
    nodes = node_tree.nodes
    links = node_tree.links

    nodes.clear()

    # Render settings
    render.use_compositing = True

    # Create necessary nodes
    render_layers_node = nodes.new(type="CompositorNodeRLayers")
    invert_node = nodes.new(type="CompositorNodeInvert")
    output_node = nodes.new(type="CompositorNodeOutputFile")

    # Connect nodes
    links.new(render_layers_node.outputs["Mist"], invert_node.inputs[1])
    links.new(invert_node.outputs[0], output_node.inputs[0])

    # Set output file path and format
    node_path = os.path.join(dir, "renders")
    output_node.base_path = bpy.path.abspath(node_path)  # Set to your desired path
    output_node.file_slots[0].path = "depth"
    output_node.format.file_format = "PNG"

    bpy.ops.render.render(write_still=True)


#
def render_depth_pass():
    save_depth_settings()
    set_depth_settings()
    render_depth_to_file()
    reset_depth_settings()
