import bpy

material_props = [
    ("TEAL", (121 / 255, 215 / 255, 219 / 255, 1)),
    ("VIOLET", (2 / 255, 0, 43 / 255, 1)),
    ("GREEN", (0, 158 / 255, 82 / 255, 1)),
    ("BLUE", (14 / 255, 125 / 255, 223 / 255, 1)),
    ("YELLOW", (255 / 255, 233 / 255, 6 / 255, 1)),
]


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
