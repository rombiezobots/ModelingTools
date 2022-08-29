##############################################################################
# Imports
##############################################################################


import bpy
from math import radians


###############################################################################
# Classes
###############################################################################


###############################################################################
# Classes
###############################################################################


class SceneProperties(bpy.types.PropertyGroup):

    scatter_objects: bpy.props.PointerProperty(name='Scatter Objects',
                                               type=bpy.types.Collection)
    container: bpy.props.PointerProperty(name='Place In',
                                         type=bpy.types.Collection)
    rot_var_x: bpy.props.FloatProperty(name='Rotation Var X',
                                       default=0.0,
                                       min=0.0,
                                       max=radians(180.0),
                                       subtype='ANGLE',
                                       unit='ROTATION')
    rot_var_y: bpy.props.FloatProperty(name='Rotation Var Y',
                                       default=0.0,
                                       min=0.0,
                                       max=radians(180.0),
                                       subtype='ANGLE', unit='ROTATION')
    rot_var_z: bpy.props.FloatProperty(name='Rotation Var Z',
                                       default=radians(180.0),
                                       min=0.0,
                                       max=radians(180.0),
                                       subtype='ANGLE', unit='ROTATION')
    scale_min: bpy.props.FloatProperty(name='Scale Min',
                                       default=0.5,
                                       min=0.0)
    scale_max: bpy.props.FloatProperty(name='Scale Max',
                                       default=1.5,
                                       min=0.0)
    dist: bpy.props.FloatProperty(name='Distance',
                                  default=0.1,
                                  min=0.0,
                                  subtype='DISTANCE',
                                  unit='LENGTH')


###############################################################################
# Registration
###############################################################################


register, unregister = bpy.utils.register_classes_factory([
    SceneProperties,
])
