import bpy
import os


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
