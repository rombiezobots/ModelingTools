##############################################################################
# Imports
##############################################################################


import bpy


##############################################################################
# Classes
##############################################################################


class VIEW3D_PT_modeling(bpy.types.Panel):

    bl_category = 'SamTools'
    bl_idname = 'VIEW3D_PT_modeling'
    bl_label = 'Modeling Tools'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        lay = self.layout
        col = lay.column(align=True)
        col.operator('modeling_tools.modeling_ot_subdiv_keep_corners',
                     icon='MOD_SUBSURF')
        col.operator('modeling_tools.modeling_ot_select_unsubdivided',
                     icon='MOD_SUBSURF')
        col.operator('modeling_tools.modeling_ot_origin_to_bottom_center',
                     icon='OBJECT_ORIGIN')


##############################################################################
# Registration
##############################################################################


classes = [
    VIEW3D_PT_modeling,
]
