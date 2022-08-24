##############################################################################
# Imports
##############################################################################


import bpy


##############################################################################
# Classes
##############################################################################


class WrapperObject(bpy.types.PropertyGroup):

    obj_name: bpy.props.StringProperty()


class SceneProperties(bpy.types.PropertyGroup):

    rotation_or_face_normals: bpy.props.EnumProperty(name='Rotation', items=[
        ('use_transforms', 'Use Object Rotation',
            'Use the objects\' transform values'),
        ('use_face_normals', 'Use First Face Normal',
            'Use the normal of the first face found in each object (Y-up)')
    ])
    batch_from: bpy.props.CollectionProperty(type=WrapperObject)
    batch_to: bpy.props.CollectionProperty(type=WrapperObject)


##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory([
    WrapperObject,
    SceneProperties,
])
