from bpy.types import Scene, UIList, PropertyGroup
from bpy.props import IntProperty, StringProperty, CollectionProperty
from bpy.utils import register_class, unregister_class


# Properties of each item in the mask list
class MaskListItem(PropertyGroup):
    mask_name: StringProperty(name="")


# Properties of each item in the mask objects list
class MaskObjectListItem(PropertyGroup):
    object_name: StringProperty(name="")


#
class PB_UL_CustomList(UIList):
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.row()
            row.label(text=item.name)
        elif self.layout_type in {"GRID"}:
            layout.alignment = "CENTER"


classes = [MaskListItem, MaskObjectListItem, PB_UL_CustomList]


def register():
    global classes
    for cls in classes:
        register_class(cls)

    Scene.mask_list = CollectionProperty(type=MaskListItem)
    Scene.mask_list_index = IntProperty(name="", default=0)


def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)

    del Scene.mask_list
    del Scene.mask_list_index