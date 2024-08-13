from .icons import icons

workflows = [
    ("SD15", "SD 1.5 {prompt}", "flux_workflow_icon"),
    ("SDXL", "SDXL {prompt}", "flux_workflow_icon"),
    ("Flux", "Flux {prompt}", "flux_workflow_icon"),
]


def get_workflow_icons(self, context):
    enum_items = []

    for i, workflow in enumerate(workflows):
        label, prompt, icon = workflow
        icon = icons["main"][icon]

        enum_items.append((prompt, label, "", icon.icon_id, i))

    return enum_items
