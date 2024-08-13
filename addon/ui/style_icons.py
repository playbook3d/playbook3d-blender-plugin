from .icons import icons

styles = [
    ("Photoreal", "Photoreal {prompt}", "photoreal_style_icon"),
    ("3DCartoon", "3D Cartoon {prompt}", "3dcartoon_style_icon"),
    ("Anime", "Anime {prompt}", "anime_style_icon"),
]


def get_style_icons():
    enum_items = []

    for style in styles:
        label, prompt, icon = style
        icon = icons[label]

        enum_items.append((prompt, label, "", icon.icon_id))

    return enum_items


def get_style_icon(icon_name):
    return icons["main"][icon_name].icon_id
