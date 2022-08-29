##############################################################################
# Imports
##############################################################################


if 'bpy' in locals():
    import importlib
    copy_transforms = importlib.reload(copy_transforms)
    scatter_paint = importlib.reload(scatter_paint)
else:
    from .copy_transforms import panels as copy_transforms
    from .scatter_paint import panels as scatter_paint
    import bpy


##############################################################################
# Classes
##############################################################################


class VIEW3D_PT_setdress(bpy.types.Panel):

    bl_category = 'SamTools'
    bl_idname = 'VIEW3D_PT_setdress'
    bl_label = 'Setdress Tools'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        lay = self.layout
        col = lay.column(align=True)
        col.operator('modeling_tools.setdress_ot_minimize_empties',
                     icon='OUTLINER_OB_EMPTY')
        col.operator('modeling_tools.setdress_ot_set_collection_instance_offset',
                     icon='OUTLINER_OB_EMPTY')
        col.operator('modeling_tools.setdress_ot_snap_rotation',
                     icon='CON_ROTLIMIT')


##############################################################################
# Registration
##############################################################################


classes = [
    VIEW3D_PT_setdress,
] + copy_transforms.classes + scatter_paint.classes
