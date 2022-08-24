##############################################################################
# Imports
##############################################################################


if 'bpy' in locals():
    import importlib
    common = importlib.reload(common)
    copy_transforms = importlib.reload(copy_transforms)
    # scatter_paint = importlib.reload(scatter_paint)
else:
    from .. import common
    from .copy_transforms import operators as copy_transforms
    # from .scatter_paint import operators as scatter_paint
    import bpy
    import math


##############################################################################
# Classes
##############################################################################


class SETDRESS_OT_minimize_empties(bpy.types.Operator):
    '''Minimize draw size for empties.\nOn selection or everything'''

    bl_idname = 'modeling_tools.setdress_ot_minimize_empties'
    bl_label = 'Minimize Empties'
    bl_options = {'UNDO'}

    def execute(self, context):
        if len(context.selected_objects) > 0:
            objects = [ob for ob in context.selected_objects
                       if ob.type == 'EMPTY'
                       and not common.is_datablock_linked(datablock=ob)]
        else:
            objects = [ob for ob in bpy.data.objects
                       if ob.type == 'EMPTY'
                       and not common.is_datablock_linked(datablock=ob)]
        for ob in objects:
            ob.empty_display_size = 0
        return {'FINISHED'}


class SETDRESS_OT_set_collection_instance_offset(bpy.types.Operator):
    '''Set the object's collections' instance offset to the object's origin.\nOn selection or everything.'''

    bl_idname = 'modeling_tools.setdress_ot_set_collection_instance_offset'
    bl_label = 'Set Collection Instance Offset'
    bl_options = {'UNDO'}

    def execute(self, context):
        if len(context.selected_objects) > 0:
            objects = [ob for ob in context.selected_objects
                       if not common.is_datablock_linked(datablock=ob)]
        else:
            objects = [ob for ob in bpy.data.objects
                       if not common.is_datablock_linked(datablock=ob)]
        for ob in objects:
            collections = [coll for coll in bpy.data.collections
                           if ob.name in coll.objects]
            for coll in collections:
                coll.instance_offset = ob.location
        return {'FINISHED'}


class SETDRESS_OT_snap_rotation(bpy.types.Operator):
    '''Snap rotation to 90-degree steps.\nOn selection or everything'''

    bl_idname = 'modeling_tools.setdress_ot_snap_rotation'
    bl_label = 'Snap Rotation'
    bl_options = {'UNDO'}

    def execute(self, context):
        if len(context.selected_objects) > 0:
            objects = [ob for ob in context.selected_objects
                       if not common.is_datablock_linked(datablock=ob)]
        else:
            objects = [ob for ob in bpy.data.objects
                       if not common.is_datablock_linked(datablock=ob)]
        for ob in objects:
            for i in range(3):
                original_in_degrees = math.degrees(ob.rotation_euler[i]) % 360
                if 45 < original_in_degrees < 90:
                    ob.rotation_euler[i] = math.radians(90)
                elif 90 < original_in_degrees < 135:
                    ob.rotation_euler[i] = math.radians(90)
                elif 135 < original_in_degrees < 180:
                    ob.rotation_euler[i] = math.radians(180)
                elif 180 < original_in_degrees < 225:
                    ob.rotation_euler[i] = math.radians(180)
                elif 225 < original_in_degrees < 270:
                    ob.rotation_euler[i] = math.radians(270)
                elif 270 < original_in_degrees < 315:
                    ob.rotation_euler[i] = math.radians(270)
                else:
                    ob.rotation_euler[i] = 0
        return {'FINISHED'}


##############################################################################
# Registration
##############################################################################


classes = [
    SETDRESS_OT_minimize_empties,
    SETDRESS_OT_set_collection_instance_offset,
    SETDRESS_OT_snap_rotation,
] + copy_transforms.classes
