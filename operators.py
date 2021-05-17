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


class SETDRESS_OT_minimize_empties(bpy.types.Operator):
    """Minimize draw size for empties.\nOn selection or everything"""

    bl_idname = 'modeling_tools.setdress_ot_minimize_empties'
    bl_label = 'Minimize Empties'
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.minimize_empties(context)
        return {'FINISHED'}


class SETDRESS_OT_set_collection_instance_offset(bpy.types.Operator):
    """Set the object's collections' instance offset to the object's origin.\nOn selection or everything."""

    bl_idname = 'modeling_tools.setdress_ot_set_collection_instance_offset'
    bl_label = 'Set Collection Instance Offset'
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.set_collection_instance_offset(context)
        return {'FINISHED'}


class SETDRESS_OT_snap_rotation(bpy.types.Operator):
    """Snap rotation to 90-degree steps.\nOn selection or everything"""

    bl_idname = 'modeling_tools.setdress_ot_snap_rotation'
    bl_label = 'Snap Rotation'
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.snap_rotation(context)
        return {'FINISHED'}


class CT_OT_delete_tt_set_a_objects(bpy.types.Operator):
    """Delete the original objects"""

    bl_idname = 'modeling_tools.ct_ot_delete_tt_set_a_objects'
    bl_label = 'Delete Original Objects'
    def execute(self, context):
        functions.delete_tt_set_a_objects(context)
        functions.clear_tt_set(context, 'a')
        return {'FINISHED'}


class CT_OT_replace_tt_set_with_selection(bpy.types.Operator):
    """Replace transfer transform list with selection of objects"""

    bl_idname = 'modeling_tools.ct_ot_replace_tt_set_with_selection'
    bl_label = 'Replace With Selection'
    tt_set: bpy.props.EnumProperty(items = [('a', 'A', 'List A'), ('b', 'B', 'List B')])

    def execute(self, context):
        functions.clear_tt_set(context, self.tt_set)
        functions.add_selection_to_tt_set(context, self.tt_set)
        return {'FINISHED'}


class CT_OT_clear_tt_set(bpy.types.Operator):
    """Clear all sharp edges in meshes.\nOn selection or everything"""

    bl_idname = 'modeling_tools.ct_ot_clear_tt_set'
    bl_label = 'Clear List'
    tt_set: bpy.props.EnumProperty(items = [('a', 'A', 'List A'), ('b', 'B', 'List B')])

    def execute(self, context):
        functions.clear_tt_set(context, self.tt_set)
        return {'FINISHED'}


class CT_OT_transfer_transforms(bpy.types.Operator):
    """Copy transformation values from a set of objects to another"""

    bl_idname = 'modeling_tools.ct_ot_transfer_transforms'
    bl_label = 'Copy Transforms'
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.transfer_transforms(context)
        return {'FINISHED'}


##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory([
    MODELING_OT_select_unsubdivided,
    SETDRESS_OT_minimize_empties,
    SETDRESS_OT_set_collection_instance_offset,
    SETDRESS_OT_snap_rotation,
    CT_OT_delete_tt_set_a_objects,
    CT_OT_replace_tt_set_with_selection,
    CT_OT_clear_tt_set,
    CT_OT_transfer_transforms,
])
