##############################################################################
# Imports
##############################################################################


if 'bpy' in locals():
    import importlib
    copy_transforms = importlib.reload(copy_transforms)
    # scatter_paint = importlib.reload(scatter_paint)
else:
    import bpy
    from .copy_transforms import properties as copy_transforms
    # from .scatter_paint import properties as scatter_paint


##############################################################################
# Classes
##############################################################################


class SceneProperties(bpy.types.PropertyGroup):
    copy_transforms: bpy.props.PointerProperty(
        type=copy_transforms.SceneProperties)
    # scatter_paint: bpy.props.PointerProperty(
    #     type=scatter_paint.SceneProperties)


##############################################################################
# Registration
##############################################################################


def register():
    copy_transforms.register()
    # scatter_paint.register()
    bpy.utils.register_class(SceneProperties)


def unregister():
    bpy.utils.unregister_class(SceneProperties)
    # scatter_paint.unregister()
    copy_transforms.unregister()
