##############################################################################
# Imports
##############################################################################


from mathutils import Vector
import bpy
import copy
import math


##############################################################################
# Functions
##############################################################################


def is_datablock_linked(datablock:bpy.types.ID) -> bool:
    return datablock.library or datablock.override_library

def clear_tt_set(context, tt_set):
    if tt_set == 'a':
        context.scene.modeling_tools.copy_transforms.set_a.clear()
    elif tt_set == 'b':
        context.scene.modeling_tools.copy_transforms.set_b.clear()
    else:
        raise RuntimeError('There\'s no active selection set.')


##############################################################################
# Operators
##############################################################################


class MODELING_OT_select_unsubdivided(bpy.types.Operator):
    '''Select all objects with a mesh data block and no subdivisions'''

    bl_idname = 'modeling_tools.modeling_ot_select_unsubdivided'
    bl_label = 'Select Unsubdivided'

    def execute(self, context):
        objects = [ob for ob in bpy.context.scene.objects if ob.type == 'MESH' and not is_datablock_linked(ob)]
        bpy.ops.object.select_all(action='DESELECT')
        for ob in objects:
            has_enabled_subsurf_modifiers = False
            for mod in ob.modifiers:
                if mod.type == 'SUBSURF':
                    has_enabled_subsurf_modifiers = mod.show_render and (mod.render_levels > 0 or ob.cycles.use_adaptive_subdivision)
                    break
            if ob.name in bpy.context.view_layer.objects:
                ob.select_set(not has_enabled_subsurf_modifiers)
        return {'FINISHED'}


class MODELING_OT_origin_to_bottom_center(bpy.types.Operator):
    '''Set the selected objects' origins to their bottom center'''

    bl_idname = 'modeling_tools.modeling_ot_origin_to_bottom_center'
    bl_label = 'Origin to Bottom Center'

    def execute(self, context):
        objects = [ob for ob in context.selected_objects if ob.type == 'MESH' and not is_datablock_linked(datablock=ob.data)]
        if len(objects) == 0:
            raise RuntimeError('This tool only works with a selection of mesh objects.')

        for ob in objects:
            bbox_ws = [ob.matrix_world @ Vector(corner) for corner in ob.bound_box]
            xmax = bbox_ws[4][0]
            xmin = bbox_ws[0][0]
            ymax = bbox_ws[3][1]
            ymin = bbox_ws[0][1]
            zmin = bbox_ws[0][2]
            x = xmax - (xmax - xmin) / 2
            y = ymax - (ymax - ymin) / 2
            cursor_original = copy.copy(context.scene.cursor.location)
            context.scene.cursor.location = (x, y, zmin)
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            context.scene.cursor.location = cursor_original
        return {'FINISHED'}


class MODELING_OT_subdiv_keep_corners(bpy.types.Operator):
    '''Enable Keep Corners on subdivision modifiers.\nOn selection or everything'''

    bl_idname = 'modeling_tools.modeling_ot_subdiv_keep_corners'
    bl_label = 'Keep Corners in Subdivision'

    def execute(self, context):
        if len(context.selected_objects) > 0:
            objects = [ob for ob in context.selected_objects if ob.type == 'MESH' and not is_datablock_linked(datablock=ob)]
        else:
            objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not is_datablock_linked(datablock=ob)]
        for ob in objects:
            subdiv_mods = [m for m in ob.modifiers if m.type == 'SUBSURF']
            for mod in subdiv_mods:
                mod.boundary_smooth = 'PRESERVE_CORNERS'
        return {'FINISHED'}


class SETDRESS_OT_minimize_empties(bpy.types.Operator):
    '''Minimize draw size for empties.\nOn selection or everything'''

    bl_idname = 'modeling_tools.setdress_ot_minimize_empties'
    bl_label = 'Minimize Empties'
    bl_options = {'UNDO'}

    def execute(self, context):
        if len(context.selected_objects) > 0:
            objects = [ob for ob in context.selected_objects if ob.type == 'EMPTY' and not is_datablock_linked(datablock=ob)]
        else:
            objects = [ob for ob in bpy.data.objects if ob.type == 'EMPTY' and not is_datablock_linked(datablock=ob)]
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
            objects = [ob for ob in context.selected_objects if not is_datablock_linked(datablock=ob)]
        else:
            objects = [ob for ob in bpy.data.objects if not is_datablock_linked(datablock=ob)]
        for ob in objects:
            collections = [coll for coll in bpy.data.collections if ob.name in coll.objects]
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
            objects = [ob for ob in context.selected_objects if not is_datablock_linked(datablock=ob)]
        else:
            objects = [ob for ob in bpy.data.objects if not is_datablock_linked(datablock=ob)]
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


class CT_OT_delete_original_objects(bpy.types.Operator):
    '''Delete the original objects'''

    bl_idname = 'modeling_tools.ct_ot_delete_original_objects'
    bl_label = 'Delete Original Objects'
    def execute(self, context):
        for wrapper_object in context.scene.modeling_tools.copy_transforms.set_a:
            if bpy.data.objects[wrapper_object.obj_name]:
                bpy.data.objects.remove(bpy.data.objects[wrapper_object.obj_name])
                print(f'Removed object {wrapper_object.obj_name}.')
        clear_tt_set(context, 'a')
        return {'FINISHED'}


class CT_OT_selection_to_tt_set(bpy.types.Operator):
    '''Replace transfer transform list with selection of objects'''

    bl_idname = 'modeling_tools.ct_ot_selection_to_tt_set'
    bl_label = 'Replace With Selection'
    tt_set: bpy.props.EnumProperty(items = [('a', 'A', 'List A'), ('b', 'B', 'List B')])

    def execute(self, context):
        clear_tt_set(context, self.tt_set)
        if self.tt_set == 'a':
            for ob in context.selected_objects:
                if not ob.library:
                    item = context.scene.modeling_tools.copy_transforms.set_a.add()
                    item.obj_name = ob.name
        elif self.tt_set == 'b':
            for ob in context.selected_objects:
                if not ob.library:
                    item = context.scene.modeling_tools.copy_transforms.set_b.add()
                    item.obj_name = ob.name
        else:
            raise RuntimeError('There\'s no active selection set.')
        return {'FINISHED'}


class CT_OT_clear_tt_set(bpy.types.Operator):
    '''Clear all sharp edges in meshes.\nOn selection or everything'''

    bl_idname = 'modeling_tools.ct_ot_clear_tt_set'
    bl_label = 'Clear List'
    tt_set: bpy.props.EnumProperty(items = [('a', 'A', 'List A'), ('b', 'B', 'List B')])

    def execute(self, context):
        clear_tt_set(context, self.tt_set)
        return {'FINISHED'}


class CT_OT_copy_transforms(bpy.types.Operator):
    '''Copy transformation values from a set of objects to another'''

    bl_idname = 'modeling_tools.ct_ot_copy_transforms'
    bl_label = 'Copy Transforms'
    bl_options = {'UNDO'}

    def execute(self, context):
        scene = context.scene
        set_a = scene.modeling_tools.copy_transforms.set_a
        set_b = scene.modeling_tools.copy_transforms.set_b

        if len(set_a) != len(set_b):
            raise RuntimeError('Both sets of objects must have equal length.')

        else:
            for ob in set_a:
                if ob.obj_name not in scene.objects.keys():
                    raise RuntimeError(f'Object {ob.obj_name} doesn\'t exist anymore.')
            for ob in set_b:
                if ob.obj_name not in scene.objects.keys():
                    raise RuntimeError(f'Object {ob.obj_name} doesn\'t exist anymore.')
            for index, ob in enumerate(set_b):
                object_a = scene.objects[set_a[index].obj_name]
                object_b = scene.objects[ob.obj_name]
                if scene.modeling_tools.copy_transforms.rotation_or_face_normals == 'use_face_normals':
                    try:
                        object_b.location = object_a.location
                        object_b.rotation_euler = object_a.data.polygons[0].normal
                        object_b.scale = object_a.scale
                    except:
                        raise RuntimeError(f'{object_a.data.name} is not a mesh, or it doesn\'t have any faces.')
                else:
                    object_b.location = object_a.location
                    object_b.rotation_euler = object_a.rotation_euler
                    object_b.scale = object_a.scale
        return {'FINISHED'}


##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory([
    CT_OT_clear_tt_set,
    CT_OT_copy_transforms,
    CT_OT_delete_original_objects,
    CT_OT_selection_to_tt_set,
    MODELING_OT_origin_to_bottom_center,
    MODELING_OT_select_unsubdivided,
    SETDRESS_OT_minimize_empties,
    SETDRESS_OT_set_collection_instance_offset,
    SETDRESS_OT_snap_rotation,
    MODELING_OT_subdiv_keep_corners,
])
