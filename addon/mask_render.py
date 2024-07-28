import bpy
import os

original_settings = {}


# Save the current color management settings
def save_mask_settings():
    scene = bpy.context.scene

    original_settings.clear()
    original_settings.update(
        {
            "display_device": scene.display_settings.display_device,
            "view_transform": scene.view_settings.view_transform,
            "look": scene.view_settings.look,
            "exposure": scene.view_settings.exposure,
            "gamma": scene.view_settings.gamma,
            "sequencer": scene.sequencer_colorspace_settings.name,
            "user_curves": scene.view_settings.use_curve_mapping,
            # "use_nodes": scene.use_nodes,
            "film_transparent": scene.render.film_transparent,
            "color_mode": scene.render.image_settings.color_mode,
            "color_depth": scene.render.image_settings.color_depth,
        }
    )


# Prepare the color management settings for render
def set_mask_settings():
    scene = bpy.context.scene
    scene.display_settings.display_device = "sRGB"
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = 0
    scene.view_settings.gamma = 1
    scene.sequencer_colorspace_settings.name = "sRGB"
    scene.view_settings.use_curve_mapping = False
    # scene.use_nodes = False
    scene.render.film_transparent = False
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "16"


# Reset the color management settings to their previous values
def reset_mask_settings():
    scene = bpy.context.scene
    scene.display_settings.display_device = original_settings["display_device"]
    scene.view_settings.view_transform = original_settings["view_transform"]
    scene.view_settings.look = original_settings["look"]
    scene.view_settings.exposure = original_settings["exposure"]
    scene.view_settings.gamma = original_settings["gamma"]
    scene.sequencer_colorspace_settings.name = original_settings["sequencer"]
    scene.view_settings.use_curve_mapping = original_settings["user_curves"]
    # scene.use_nodes = original_settings["use_nodes"]
    scene.render.film_transparent = original_settings["film_transparent"]
    scene.render.image_settings.color_mode = original_settings["color_mode"]
    scene.render.image_settings.color_depth = original_settings["color_depth"]


#
def render_mask_to_file():
    scene = bpy.context.scene
    render = scene.render

    dir = os.path.dirname(__file__)

    output_path = os.path.join(dir, "renders", "mask.png")
    render.filepath = output_path

    if scene.camera:
        bpy.ops.render.render(write_still=True)
        # bpy.ops.render.view_show("INVOKE_DEFAULT")
    else:
        print("No active camera found in the scene")
