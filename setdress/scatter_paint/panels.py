##############################################################################
# Imports
##############################################################################


import bpy
from math import radians


###############################################################################
# Classes
###############################################################################


class VIEW3D_PT_scatter_paint(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_scatter_paint'
    bl_label = 'Scatter Paint'
    bl_space_type = 'VIEW_3D'
    bl_parent_id = 'VIEW3D_PT_setdress'
    bl_region_type = 'UI'

    def draw(self, context):
        sp = context.scene.modeling_tools.setdress.scatter_paint
        lay = self.layout
        lay.use_property_split = True
        lay.use_property_decorate = False

        col = lay.column(align=True)
        col.prop(sp, 'scatter_objects')
        col.prop(sp, 'container')
        col = lay.column(align=True)
        col.prop(sp, 'rot_var_x')
        col.prop(sp, 'rot_var_y', text='Y')
        col.prop(sp, 'rot_var_z', text='Z')
        col = lay.column(align=True)
        col.prop(sp, 'scale_min')
        col.prop(sp, 'scale_max', text='Max')
        col = lay.column(align=True)
        col.prop(sp, 'dist')
        row = lay.row()
        row.scale_y = 1.5
        row.operator('modeling_tools.sp_ot_scatter_paint',
                     icon='BRUSH_DATA')


###############################################################################
# Registration
###############################################################################


classes = [
    VIEW3D_PT_scatter_paint,
]
