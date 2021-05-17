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


class WrapperObject(bpy.types.PropertyGroup):
    obj_name: bpy.props.StringProperty()


##############################################################################
# Registration
##############################################################################


def register():
    bpy.utils.register_class(ModelingToolsSettings)
    bpy.utils.register_class(WrapperObject)
    bpy.types.Scene.modeling_tools_settings = bpy.props.PointerProperty(type=ModelingToolsSettings)
    bpy.types.Scene.modeling_tools_ct_set_a = bpy.props.CollectionProperty(type = WrapperObject)
    bpy.types.Scene.modeling_tools_ct_set_a_index = bpy.props.IntProperty(default = 0)
    bpy.types.Scene.modeling_tools_ct_set_b = bpy.props.CollectionProperty(type = WrapperObject)
    bpy.types.Scene.modeling_tools_ct_set_b_index = bpy.props.IntProperty(default = 0)


def unregister():
    bpy.utils.unregister_class(ModelingToolsSettings)
    bpy.utils.unregister_class(WrapperObject)
    try:
        del bpy.types.Scene.modeling_tools_settings
        del bpy.types.Scene.modeling_tools_ct_set_a
        del bpy.types.Scene.modeling_tools_ct_set_b
    except:
        pass
