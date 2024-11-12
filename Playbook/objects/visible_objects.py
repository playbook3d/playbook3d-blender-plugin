from .objects import visible_objects, hidden_objects

allowed_obj_types = ["MESH", "FONT", "META", "SURFACE"]


# Get all visible objects in the scene
def set_visible_objects(context):
    visible_objects.clear()
    for obj in context.scene.objects:

        if obj.hide_render:
            continue

        # Object is not visible. Ignore
        if obj.hide_get():
            obj.hide_render = True
            hidden_objects.append(obj)
            continue

        if obj.type in allowed_obj_types:
            visible_objects.append(obj)


#
def reset_visible_objects():
    visible_objects.clear()

    for obj in hidden_objects:
        obj.hide_render = False
