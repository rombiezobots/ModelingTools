##############################################################################
# Imports
##############################################################################


import bpy
from . import functions
from importlib import reload
reload(functions)


##############################################################################
# Properties
##############################################################################


class ModelingToolsSettings(bpy.types.PropertyGroup):

    pass


##############################################################################
# Registration
##############################################################################


def register():
    bpy.utils.register_class(ModelingToolsSettings)
    bpy.types.Scene.modeling_tools_settings = bpy.props.PointerProperty(type=ModelingToolsSettings)


def unregister():
    bpy.utils.unregister_class(ModelingToolsSettings)
    try:
        del bpy.types.Scene.modeling_tools_settings
    except:
        pass
