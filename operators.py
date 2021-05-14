##############################################################################
# Imports
##############################################################################


import bpy
from . import functions
from importlib import reload
reload(functions)


##############################################################################
# Operators
##############################################################################


class MODELING_OT_select_unsubdivided(bpy.types.Operator):
    """Select all objects with a mesh data block and no subdivisions"""

    bl_idname = "modeling_tools.modeling_ot_select_unsubdivided"
    bl_label = "Select Unsubdivided"

    def execute(self, context):
        functions.select_unsubdivided()
        return {'FINISHED'}


##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory([
    MODELING_OT_select_unsubdivided
])
