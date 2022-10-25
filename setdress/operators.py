##############################################################################
# Imports
##############################################################################


from email.policy import default


if 'bpy' in locals():
    import importlib
    common = importlib.reload(common)
    copy_transforms = importlib.reload(copy_transforms)
    scatter_paint = importlib.reload(scatter_paint)
else:
    from .. import common
    from .copy_transforms import operators as copy_transforms
    from .scatter_paint import operators as scatter_paint
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
    '''Snap rotation to custom steps.\nOn selection or everything'''

    bl_idname = 'modeling_tools.setdress_ot_snap_rotation'
    bl_label = 'Snap Rotation'
    bl_options = {'REGISTER', 'UNDO'}

    step_x: bpy.props.FloatProperty(name='Step X',
                                    default=math.radians(90),
                                    subtype='ANGLE',
                                    unit='ROTATION')
    step_y: bpy.props.FloatProperty(name='Step Y',
                                    default=math.radians(90),
                                    subtype='ANGLE',
                                    unit='ROTATION')
    step_z: bpy.props.FloatProperty(name='Step Z',
                                    default=math.radians(90),
                                    subtype='ANGLE',
                                    unit='ROTATION')
    do_x: bpy.props.BoolProperty(name='X')
    do_y: bpy.props.BoolProperty(name='Y')
    do_z: bpy.props.BoolProperty(name='Z', default=True)

    def draw(self, context):
        lay = self.layout
        lay.prop(self, 'space')
        col = lay.column(align=True)
        row = col.row(align=True)
        row.prop(self, 'do_x', text='X', icon='EMPTY_AXIS')
        row.prop(self, 'step_x', text='')
        row = col.row(align=True)
        row.prop(self, 'do_y', text='Y', icon='EMPTY_AXIS')
        row.prop(self, 'step_y', text='')
        row = col.row(align=True)
        row.prop(self, 'do_z', text='Z', icon='EMPTY_AXIS')
        row.prop(self, 'step_z', text='')

    def execute(self, context):
        if len(context.selected_objects) > 0:
            objects = [ob for ob in context.selected_objects
                       if not common.is_datablock_linked(datablock=ob)]
        else:
            objects = [ob for ob in bpy.data.objects
                       if not common.is_datablock_linked(datablock=ob)]
        map = [
            (self.do_x, self.step_x),
            (self.do_y, self.step_y),
            (self.do_z, self.step_z)
        ]
        for ob in objects:
            for i, tup in enumerate(map):
                if tup[0]:
                    orig = ob.rotation_euler[i]
                    ob.rotation_euler[i] = tup[1] * round(orig / tup[1])
        return {'FINISHED'}


##############################################################################
# Registration
##############################################################################


classes = [
    SETDRESS_OT_minimize_empties,
    SETDRESS_OT_set_collection_instance_offset,
    SETDRESS_OT_snap_rotation,
] + copy_transforms.classes + scatter_paint.classes
