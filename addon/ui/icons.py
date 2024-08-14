import os
from bpy.utils import previews

icons = {}


def get_workflow_icon(icon_name):
    return icons["main"][icon_name].icon_id


# def get_style_icons():
#     enum_items = []

#     for style in styles:
#         label, prompt, icon = style
#         icon = icons[label]

#         enum_items.append((prompt, label, "", icon.icon_id))

#     return enum_items


def get_style_icon(icon_name):
    return icons["main"][icon_name].icon_id


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

    # Workspace icons
    new_icons.load(
        "retexture_workflow_icon",
        os.path.join(icons_dir, "retexture_workflow.png"),
        "IMAGE",
    )
    new_icons.load(
        "style_transfer_workflow_icon",
        os.path.join(icons_dir, "style_transfer_workflow.png"),
        "IMAGE",
    )

    # Style icons
    new_icons.load(
        "photoreal_style_icon", os.path.join(icons_dir, "photoreal_style.png"), "IMAGE"
    )
    new_icons.load(
        "3dcartoon_style_icon", os.path.join(icons_dir, "3dcartoon_style.png"), "IMAGE"
    )
    new_icons.load(
        "anime_style_icon", os.path.join(icons_dir, "anime_style.png"), "IMAGE"
    )

    icons["main"] = new_icons


def unregister():
    # Clear custom icons
    for icon in icons.values():
        previews.remove(icon)

    del icons["main"]
