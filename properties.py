##############################################################################
# Imports
##############################################################################


if 'bpy' in locals():
    import importlib
    setdress = importlib.reload(setdress)
else:
    import bpy
    from .setdress import properties as setdress


##############################################################################
# Classes
##############################################################################


class SceneProperties(bpy.types.PropertyGroup):

    setdress: bpy.props.PointerProperty(
        type=setdress.SceneProperties)


##############################################################################
# Registration
##############################################################################


def register():
    setdress.register()
    bpy.utils.register_class(SceneProperties)
    bpy.types.Scene.modeling_tools = bpy.props.PointerProperty(
        type=SceneProperties, name='Modeling Tools')


def unregister():
    del bpy.types.Scene.modeling_tools
    bpy.utils.unregister_class(SceneProperties)
    setdress.unregister()
