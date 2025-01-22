import os
from bpy.utils import previews

icons = {}


# Custom icons
def register():
    new_icons = previews.new()
    icons_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
    new_icons.load(
        "playbook_logo", os.path.join(icons_dir, "playbook_logo.png"), "IMAGE"
    )
    new_icons.load(
        "playbook_logo_main", os.path.join(icons_dir, "playbook_logo_main.png"), "IMAGE"
    )
    new_icons.load("discord_logo", os.path.join(icons_dir, "discord_logo.png"), "IMAGE")
    new_icons.load("twitter_logo", os.path.join(icons_dir, "twitter_logo.png"), "IMAGE")
    new_icons.load("check_icon", os.path.join(icons_dir, "check_icon.png"), "IMAGE")
    new_icons.load("credit_icon", os.path.join(icons_dir, "credit_icon.png"), "IMAGE")

    icons["main"] = new_icons


def unregister():
    # Clear custom icons
    for icon in icons.values():
        previews.remove(icon)

    del icons["main"]
