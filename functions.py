##############################################################################
# Imports
##############################################################################


import bpy
import math


##############################################################################
# Functions
##############################################################################


def is_datablock_linked(datablock:bpy.types.ID) -> bool:
    return datablock.library or datablock.override_library


def select_unsubdivided():
    objects = [ob for ob in bpy.context.scene.objects if ob.type == 'MESH' and not is_datablock_linked(ob)]
    bpy.ops.object.select_all(action = 'DESELECT')
    for ob in objects:
        has_enabled_subsurf_modifiers = False
        for mod in ob.modifiers:
            if mod.type == 'SUBSURF':
                has_enabled_subsurf_modifiers = mod.show_render and (mod.render_levels > 0 or ob.cycles.use_adaptive_subdivision)
                break
        if ob.name in bpy.context.view_layer.objects:
            ob.select_set(not has_enabled_subsurf_modifiers)


def add_selection_to_tt_set(context, tt_set):
    """Add selection of objects to the transfer transforms lists"""

    if tt_set == 'a':
        for ob in context.selected_objects:
            if not ob.library:
                item = context.scene.modeling_tools_ct_set_a.add()
                item.obj_name = ob.name
    elif tt_set == 'b':
        for ob in context.selected_objects:
            if not ob.library:
                item = context.scene.modeling_tools_ct_set_b.add()
                item.obj_name = ob.name
    else:
        raise RuntimeError("There's no active selection set.")


def clear_tt_set(context, tt_set):
    """Clear all sharp edges in meshes.\nOn selection or everything"""

    if tt_set == 'a':
        context.scene.modeling_tools_ct_set_a.clear()
    elif tt_set == 'b':
        context.scene.modeling_tools_ct_set_b.clear()
    else:
        raise RuntimeError("There's no active selection set.")


def delete_tt_set_a_objects(context):
    """Delete the original objects"""

    for wrapper_object in context.scene.modeling_tools_ct_set_a:
        if bpy.data.objects[wrapper_object.obj_name]:
            bpy.data.objects.remove(bpy.data.objects[wrapper_object.obj_name])
            print(f"Removed object {wrapper_object.obj_name}.")


def minimize_empties(context):
    """Minimize draw size for empties.\nOn selection or everything"""

    if len(context.selected_objects) > 0:
        objects = [ob for ob in context.selected_objects if ob.type == 'EMPTY' and not ob.library]
    else:
        objects = [ob for ob in bpy.data.objects if ob.type == 'EMPTY' and not ob.library]

    for ob in objects:
        ob.empty_display_size = 0


def set_collection_instance_offset(context):
    """Set the object's collections' instance offset to the object's origin.\nOn selection or everything"""

    if len(context.selected_objects) > 0:
        objects = [ob for ob in context.selected_objects if not ob.library]
    else:
        objects = [ob for ob in bpy.data.objects if not ob.library]

    for ob in objects:
        collections = [coll for coll in bpy.data.collections if ob.name in coll.objects]
        for coll in collections:
            coll.instance_offset = ob.location


def snap_rotation(context):
    """Snap rotation to 90-degree steps"""

    if len(context.selected_objects) > 0:
        objects = [ob for ob in context.selected_objects if not ob.library]
    else:
        objects = [ob for ob in bpy.data.objects if not ob.library]

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


def transfer_transforms(context):
    """Copy transformation values from a set of objects to another"""

    set_a = context.scene.modeling_tools_ct_set_a
    set_b = context.scene.modeling_tools_ct_set_b

    if len(set_a) != len(set_b):
        raise RuntimeError("Both sets of objects must have equal length.")

    else:
        for ob in set_a:
            if ob.obj_name not in context.scene.objects.keys():
                raise RuntimeError(f"Object '{ob.obj_name}' doesn't exist anymore.")
        for ob in set_b:
            if ob.obj_name not in context.scene.objects.keys():
                raise RuntimeError(f"Object '{ob.obj_name}' doesn't exist anymore.")
        for index, ob in enumerate(set_b):
            object_a = context.scene.objects[set_a[index].obj_name]
            object_b = context.scene.objects[ob.obj_name]
            object_b.location = object_a.location
            object_b.rotation_euler = object_a.rotation_euler
            object_b.scale = object_a.scale


def get_active_object_collection_offset(self) -> tuple:
    active_object_is_in_collection = None
    obj = bpy.context.active_object
    for collection in bpy.data.collections:
        collection_objects = collection.objects
        if obj.name in collection.objects and obj in collection_objects[:]:
            active_object_is_in_collection = collection
            break
    if not active_object_is_in_collection:
        return None
    return collection.instance_offset
