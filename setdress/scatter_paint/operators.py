##############################################################################
# Imports
##############################################################################


import bpy
import bmesh
import mathutils
from bpy_extras import view3d_utils
import random


###############################################################################
# Functions
###############################################################################


def bvhtree_from_object(object):
    bm = bmesh.new()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    object_eval = object.evaluated_get(depsgraph)
    mesh = object_eval.to_mesh()
    bm.from_mesh(mesh)
    bm.transform(object.matrix_world)
    bvhtree = mathutils.bvhtree.BVHTree.FromBMesh(bm)
    object_eval.to_mesh_clear()
    return bvhtree


def currently_in_3d_view(context):
    return


def event_is_in_region(event, region):
    return (region.x <= event.mouse_x <= region.x + region.width
            and region.y <= event.mouse_y <= region.y + region.height)


def get_largest_dimension(ob):
    return max(ob.dimensions[0], ob.dimensions[1], ob.dimensions[2])


def get_variance(x, y, z):
    return mathutils.Vector((
        random.uniform(-x, x),
        random.uniform(-y, y),
        random.uniform(-z, z)
    ))


def raycast(surface, pos_screen):
    bvhtree = bvhtree_from_object(surface)
    region = bpy.context.region
    region_3d = bpy.context.space_data.region_3d
    origin = view3d_utils.region_2d_to_origin_3d(
        region, region_3d, pos_screen)
    direction = view3d_utils.region_2d_to_vector_3d(
        region, region_3d, pos_screen)
    location, normal, index, distance = bvhtree.ray_cast(origin, direction)
    return location, normal, index, distance


###############################################################################
# Classes
###############################################################################


class SP_OT_scatter_paint(bpy.types.Operator):
    '''Scatter the selected objects onto the active object's surface as you paint'''

    bl_idname = 'modeling_tools.sp_ot_scatter_paint'
    bl_label = 'Paint'
    bl_options = {'REGISTER', 'UNDO'}

    is_painting: bpy.props.BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        sp = context.scene.modeling_tools.setdress.scatter_paint
        if not sp.scatter_objects and context.active_object:
            return False
        return (len(sp.scatter_objects.objects) > 0
                and context.space_data.type == 'VIEW_3D'
                and sp.container
                and context.active_object.type == 'MESH')

    def invoke(self, context, event):
        self.last_instance = None
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):

        sp = context.scene.modeling_tools.setdress.scatter_paint
        bpy.context.window.cursor_set(cursor='PAINT_CROSS')

        # Ignore clicking outside the viewport when there's no stroke yet.
        if not event_is_in_region(event, context.region):
            return {'PASS_THROUGH'}

        # Exit on pressing Escape or Enter, or right-clicking.
        if event.type in ['ESC', 'RET', ]:
            # bpy.context.area.tag_redraw()
            bpy.context.window.cursor_set(cursor='DEFAULT')
            return {'FINISHED'}

        # Set the self.is_painting boolean depending on what the mouse is doing.
        elif event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                self.is_painting = True
            elif event.value == 'RELEASE':
                self.is_painting = False

        if self.is_painting:
            # Cast a ray from the current screen pixel to the target mesh. From
            # the resulting point, extract the position and normal.
            pos_screen = (event.mouse_region_x, event.mouse_region_y)
            pos_world, normal, *_ = raycast(surface=context.active_object,
                                            pos_screen=pos_screen)
            # If we hit the target surface:
            if pos_world:
                # Measure how far we are from the last instance. If there's
                # none, or the distance is larger than sp.dist, create an
                # instance now.
                if self.distance_from_last_instance(pos=pos_world) >= sp.dist:
                    self.last_instance = self.create_next_instance(
                        pos=pos_world, normal=normal)
            return {'RUNNING_MODAL'}

        # Idle when doing anything else, so we can still pan, rotate and dolly
        # the viewport.
        return {'PASS_THROUGH'}

    def distance_from_last_instance(self, pos):
        # TODO: if the object is not an empty, camera, ... also take largest
        # dimension into account.
        if not self.last_instance:
            return True
        difference = pos - self.last_instance.location
        return difference.length

    def create_next_instance(self, pos, normal):
        # Check which object was the last one we used to instantiate, and pick
        # the next object in the collection.
        sp = bpy.context.scene.modeling_tools.setdress.scatter_paint
        objects = sp.scatter_objects.objects
        next_src_ob = objects[0]
        # Create an instance of the object.
        instance = bpy.data.objects.new(name=next_src_ob.name,
                                        object_data=next_src_ob.data)
        instance.location = pos
        instance.rotation_euler = normal + get_variance(x=sp.rot_var_x,
                                                        y=sp.rot_var_y,
                                                        z=sp.rot_var_z)
        instance.scale[0] = instance.scale[1] = instance.scale[2] = random.uniform(
            a=sp.scale_min, b=sp.scale_max)
        sp.container.objects.link(instance)
        # If the object is an empty, copy its instancing settings, if any.
        if next_src_ob.type == 'EMPTY':
            instance.instance_type = next_src_ob.instance_type
            instance.instance_collection = next_src_ob.instance_collection
        return instance


###############################################################################
# Registration
###############################################################################


classes = [
    SP_OT_scatter_paint,
]
