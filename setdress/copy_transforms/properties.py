##############################################################################
# Imports
##############################################################################


import bpy


##############################################################################
# Classes
##############################################################################


class SceneProperties(bpy.types.PropertyGroup):

    collection_from: bpy.props.PointerProperty(type=bpy.types.Collection,
                                               name='From',
                                               description='Collection of objects to copy transforms from')
    collection_to: bpy.props.PointerProperty(type=bpy.types.Collection,
                                             name='To',
                                             description='Collection of objects to copy transforms to')


##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory([
    SceneProperties,
])
