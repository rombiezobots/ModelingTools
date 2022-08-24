##############################################################################
# Imports
##############################################################################


if 'bpy' in locals():
    import importlib
    common = importlib.reload(common)
else:
    from .. import common
    from mathutils import Vector
    import copy
    import bpy


##############################################################################
# Classes
##############################################################################


class MODELING_OT_select_unsubdivided(bpy.types.Operator):
    '''Select all objects with a mesh data block and no subdivisions'''

    bl_idname = 'modeling_tools.modeling_ot_select_unsubdivided'
    bl_label = 'Select Unsubdivided'

    def execute(self, context):
        objects = [ob for ob in bpy.context.scene.objects
                   if ob.type == 'MESH'
                   and not common.is_datablock_linked(ob)]
        bpy.ops.object.select_all(action='DESELECT')
        for ob in objects:
            has_enabled_subsurf_modifiers = False
            for mod in ob.modifiers:
                if mod.type == 'SUBSURF':
                    has_enabled_subsurf_modifiers = mod.show_render and (
                        mod.render_levels > 0 or
                        ob.cycles.use_adaptive_subdivision)
                    break
            if ob.name in bpy.context.view_layer.objects:
                ob.select_set(not has_enabled_subsurf_modifiers)
        return {'FINISHED'}


class MODELING_OT_origin_to_bottom_center(bpy.types.Operator):
    '''Set the selected objects' origins to their bottom center'''

    bl_idname = 'modeling_tools.modeling_ot_origin_to_bottom_center'
    bl_label = 'Origin to Bottom Center'

    def execute(self, context):
        objects = [ob for ob in context.selected_objects
                   if ob.type == 'MESH'
                   and not common.is_datablock_linked(datablock=ob.data)]
        if len(objects) == 0:
            raise RuntimeError(
                'This tool only works with a selection of mesh objects.')

         # Deselect all objects first, otherwise each of their origins will be
        # overwritten by the current object in the loop. Also save a copy of the
        # 3D Cursor's location.
        for ob in objects:
            ob.select_set(False)
        cursor_original = copy.copy(context.scene.cursor.location)

        # Loop over each object.
        for ob in objects:
            # Calculate the world space coordinates of its bounding box, take
            # half of its width and depth, and its lowest point.
            bbox_ws = [ob.matrix_world @ Vector(corner)
                       for corner in ob.bound_box]
            xmax = bbox_ws[4][0]
            xmin = bbox_ws[0][0]
            ymax = bbox_ws[3][1]
            ymin = bbox_ws[0][1]
            zmin = bbox_ws[0][2]
            x = xmax - (xmax - xmin) / 2
            y = ymax - (ymax - ymin) / 2

            # Snap the 3D cursor to these coordinates, select the object, set its
            # origin, and deselect it again.
            context.scene.cursor.location = (x, y, zmin)
            ob.select_set(True)
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            ob.select_set(False)

        # Select the list of objects again, and restore the 3D Cursor.
        for ob in objects:
            ob.select_set(True)
        context.scene.cursor.location = cursor_original

        return {'FINISHED'}


class MODELING_OT_subdiv_keep_corners(bpy.types.Operator):
    '''Enable Keep Corners on subdivision modifiers.\nOn selection or everything'''

    bl_idname = 'modeling_tools.modeling_ot_subdiv_keep_corners'
    bl_label = 'Keep Corners in Subdivision'

    def execute(self, context):
        if len(context.selected_objects) > 0:
            objects = [ob for ob in context.selected_objects
                       if ob.type == 'MESH'
                       and not common.is_datablock_linked(datablock=ob)]
        else:
            objects = [ob for ob in bpy.data.objects
                       if ob.type == 'MESH'
                       and not common.is_datablock_linked(datablock=ob)]
        for ob in objects:
            subdiv_mods = [m for m in ob.modifiers if m.type == 'SUBSURF']
            for mod in subdiv_mods:
                mod.boundary_smooth = 'PRESERVE_CORNERS'
        return {'FINISHED'}


class MODELING_OT_subdiv_disable_in_edit_mode(bpy.types.Operator):
    '''Disable Subdivision modifiers in Edit Mode.\nOn selection or everything'''

    bl_idname = 'modeling_tools.modeling_ot_subdiv_disable_in_edit_mode'
    bl_label = 'Disable Subdiv in Edit Mode'

    def execute(self, context):
        if len(context.selected_objects) > 0:
            objects = [ob for ob in context.selected_objects
                       if ob.type == 'MESH'
                       and not common.is_datablock_linked(datablock=ob)]
        else:
            objects = [ob for ob in bpy.data.objects
                       if ob.type == 'MESH'
                       and not common.is_datablock_linked(datablock=ob)]
        for ob in objects:
            subdiv_mods = [m for m in ob.modifiers if m.type == 'SUBSURF']
            for mod in subdiv_mods:
                mod.show_in_editmode = False
        return {'FINISHED'}


##############################################################################
# Registration
##############################################################################


classes = [
    MODELING_OT_origin_to_bottom_center,
    MODELING_OT_select_unsubdivided,
    MODELING_OT_subdiv_keep_corners,
    MODELING_OT_subdiv_disable_in_edit_mode,
]
