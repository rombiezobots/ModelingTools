##############################################################################
# Imports
##############################################################################


import bpy


##############################################################################
# Functions
##############################################################################


def clear_batch(context, batch: str):
    ct = context.scene.modeling_tools.setdress.copy_transforms
    if batch == 'a':
        ct.batch_from.clear()
    elif batch == 'b':
        ct.batch_to.clear()
    else:
        raise RuntimeError('There\'s no active selection batch.')


##############################################################################
# Classes
##############################################################################


class CT_OT_delete_original_objects(bpy.types.Operator):
    '''Delete the original objects'''

    bl_idname = 'modeling_tools.ct_ot_delete_original_objects'
    bl_label = 'Delete Original Objects'

    def execute(self, context):
        ct = context.scene.modeling_tools.setdress.copy_transforms
        for wrapper_object in ct.batch_from:
            if wrapper_object.obj_name in bpy.data.objects.keys():
                ob = bpy.data.objects[wrapper_object.obj_name]
                bpy.data.objects.remove(ob)
                print(f'Removed object {wrapper_object.obj_name}.')
        clear_batch(context, batch='a')
        return {'FINISHED'}


class CT_OT_selection_to_batch(bpy.types.Operator):
    '''Replace transfer transform list with selection of objects'''

    bl_idname = 'modeling_tools.ct_ot_selection_to_batch'
    bl_label = 'Replace With Selection'
    batch: bpy.props.EnumProperty(items=[
        ('a', 'A', 'List A'),
        ('b', 'B', 'List B')
    ])

    def execute(self, context):
        ct = context.scene.modeling_tools.setdress.copy_transforms
        clear_batch(context, batch=self.batch)
        if self.batch == 'a':
            for ob in context.selected_objects:
                if not ob.library:
                    item = ct.batch_from.add()
                    item.obj_name = ob.name
        elif self.batch == 'b':
            for ob in context.selected_objects:
                if not ob.library:
                    item = ct.batch_to.add()
                    item.obj_name = ob.name
        else:
            raise RuntimeError('There\'s no active selection set.')
        return {'FINISHED'}


class CT_OT_clear_batch(bpy.types.Operator):
    '''Clear object batch'''

    bl_idname = 'modeling_tools.ct_ot_clear_batch'
    bl_label = 'Clear Batch'
    batch: bpy.props.EnumProperty(items=[
        ('a', 'A', 'Batch A'),
        ('b', 'B', 'Batch B')
    ])

    def execute(self, context):
        clear_batch(context, batch=self.batch)
        return {'FINISHED'}


class CT_OT_copy_transforms(bpy.types.Operator):
    '''Copy transformation values from a set of objects to another'''

    bl_idname = 'modeling_tools.ct_ot_copy_transforms'
    bl_label = 'Copy Transforms'
    bl_options = {'UNDO'}

    def execute(self, context):
        ct = context.scene.modeling_tools.setdress.copy_transforms
        batch_from = ct.batch_from
        batch_to = ct.batch_to

        if len(batch_from) != len(batch_to):
            raise RuntimeError('Both sets of objects must have equal length.')

        else:
            for ob in batch_from:
                if ob.obj_name not in context.scene.objects.keys():
                    raise RuntimeError(
                        f'Object {ob.obj_name} doesn\'t exist anymore.')
            for ob in batch_to:
                if ob.obj_name not in context.scene.objects.keys():
                    raise RuntimeError(
                        f'Object {ob.obj_name} doesn\'t exist anymore.')
            for index, ob in enumerate(batch_to):
                ob_a = context.scene.objects[batch_from[index].obj_name]
                ob_b = context.scene.objects[ob.obj_name]
                if ct.rotation_or_face_normals == 'use_face_normals':
                    try:
                        ob_b.location = ob_a.location
                        ob_b.rotation_euler = ob_a.data.polygons[0].normal
                        ob_b.scale = ob_a.scale
                    except:
                        raise RuntimeError(
                            f'{ob_a.data.name} is not a mesh, or it doesn\'t have any faces.')
                else:
                    ob_b.location = ob_a.location
                    ob_b.rotation_euler = ob_a.rotation_euler
                    ob_b.scale = ob_a.scale
        return {'FINISHED'}


##############################################################################
# Registration
##############################################################################


classes = [
    CT_OT_selection_to_batch,
    CT_OT_delete_original_objects,
    CT_OT_copy_transforms,
    CT_OT_clear_batch,
]
