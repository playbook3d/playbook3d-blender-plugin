import bpy
import base64

original_settings = {}


# Save the current color management settings
def save_style_settings():
    scene = bpy.context.scene

    original_settings.clear()
    original_settings.update(
        {
            "display_device": scene.display_settings.display_device,
            "view_transform": scene.view_settings.view_transform,
            "color_mode": scene.render.image_settings.color_mode,
            "color_depth": scene.render.image_settings.color_depth,
        }
    )


# Prepare the color management settings for render
def set_style_settings():
    scene = bpy.context.scene
    scene.display_settings.display_device = "sRGB"
    scene.view_settings.view_transform = "Standard"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "16"


# Reset the color management settings to their previous values
def reset_style_settings():
    scene = bpy.context.scene
    scene.display_settings.display_device = original_settings["display_device"]
    scene.view_settings.view_transform = original_settings["view_transform"]
    scene.render.image_settings.color_mode = original_settings["color_mode"]
    scene.render.image_settings.color_depth = original_settings["color_depth"]


#
def render_style_to_file(image, filepath: str):
    # Save the image as PNG
    image.filepath_raw = filepath
    image.file_format = "PNG"
    image.save_render(filepath)

    # Read the file and encode to Base64
    with open(filepath, "rb") as image_file:
        byte_data = image_file.read()

    return base64.b64encode(byte_data)


#
def render_style_transfer_pass(image, filepath):
    save_style_settings()
    set_style_settings()
    style_image = render_style_to_file(image, filepath)
    reset_style_settings()

    return style_image
