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
        pass


class VIEW3D_PT_subdivision(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_subdivision'
    bl_label = 'Subdivision'
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'VIEW3D_PT_modeling'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        lay = self.layout
        col = lay.column(align=True)
        col.operator('modeling_tools.modeling_ot_select_unsubdivided',
                     icon='MOD_SUBSURF')
        col.operator('modeling_tools.modeling_ot_subdiv_disable_in_edit_mode',
                     icon='MOD_SUBSURF')
        col.operator('modeling_tools.modeling_ot_subdiv_keep_corners',
                     icon='MOD_SUBSURF')


class VIEW3D_PT_origins(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_origins'
    bl_label = 'Origins'
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'VIEW3D_PT_modeling'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        lay = self.layout
        col = lay.column(align=True)
        col.operator('modeling_tools.modeling_ot_origin_to_bottom_center',
                     icon='OBJECT_ORIGIN')
        col.operator('modeling_tools.modeling_ot_align_pivot_to_transform_orient',
                     icon='ORIENTATION_LOCAL')


##############################################################################
# Registration
##############################################################################


classes = [
    VIEW3D_PT_modeling,
    VIEW3D_PT_origins,
    VIEW3D_PT_subdivision,
]
