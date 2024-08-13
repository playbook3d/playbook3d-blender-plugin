import bpy
import os


def get_filepath_in_package(path, filename=""):
    # Convert a relative path in the add-on package to an absolute path
    addon_path = os.path.dirname(os.path.realpath(__file__))
    subpath = path + os.sep + filename if path else filename

    return os.path.join(addon_path, subpath)


# Create a new simple RGB material
def create_rgb_material(name, color):
    mat = bpy.data.materials.new(name=name)

    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear the material's nodes
    for node in nodes:
        nodes.remove(node)

    rgb_node = nodes.new(type="ShaderNodeRGB")
    rgb_node.outputs["Color"].default_value = color

    material_output = nodes.new(type="ShaderNodeOutputMaterial")

    # Link the created nodes
    mat.node_tree.links.new(
        rgb_node.outputs["Color"], material_output.inputs["Surface"]
    )

    return mat
