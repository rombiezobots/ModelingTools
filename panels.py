##############################################################################
# Imports
##############################################################################


import bpy


##############################################################################
# Panels
##############################################################################


class VIEW3D_PT_modeling_tools(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_modeling_tools'
    bl_label = 'Modeling and Setdress Tools'
    bl_category = 'SamTools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        lay = self.layout

class VIEW3D_PT_modeling(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_modeling'
    bl_label = 'Modeling'
    bl_parent_id = 'VIEW3D_PT_modeling_tools'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        lay = self.layout
        lay.use_property_decorate = False
        lay.operator('modeling_tools.modeling_ot_select_unsubdivided', icon='MOD_SUBSURF')


class VIEW3D_PT_setdress(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_setdress'
    bl_label = 'Setdress'
    bl_parent_id = 'VIEW3D_PT_modeling_tools'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        lay = self.layout
        col = lay.column(align=True)
        col.operator('modeling_tools.setdress_ot_minimize_empties', icon = 'OUTLINER_OB_EMPTY')
        col.operator('modeling_tools.setdress_ot_set_collection_instance_offset', icon = 'OUTLINER_OB_EMPTY')
        lay.operator('modeling_tools.setdress_ot_snap_rotation', icon = 'CON_ROTLIMIT')


class VIEW3D_PT_copy_transforms(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_copy_transforms'
    bl_label = 'Copy Transforms'
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'VIEW3D_PT_modeling_tools'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        lay = self.layout
        col = lay.column(align = True)
        row_a = col.row(align = True)
        row_a.operator('modeling_tools.ct_ot_clear_tt_set', icon = 'X', text = '').tt_set = 'a'
        row_a.operator('modeling_tools.ct_ot_replace_tt_set_with_selection', text = f'From {len(context.scene.modeling_tools_ct_set_a)} objects').tt_set = 'a'
        row_go = col.row(align = True)
        row_go.scale_y = 1.5
        row_go.operator('modeling_tools.ct_ot_transfer_transforms', icon = 'TRIA_DOWN')
        row_b = col.row(align = True)
        row_b.operator('modeling_tools.ct_ot_clear_tt_set', icon = 'X', text = '').tt_set = 'b'
        row_b.operator('modeling_tools.ct_ot_replace_tt_set_with_selection', text = f'To {len(context.scene.modeling_tools_ct_set_b)} objects').tt_set = 'b'
        col.separator()
        col.operator('modeling_tools.ct_ot_delete_tt_set_a_objects', icon = 'X')


##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory([
    VIEW3D_PT_modeling_tools,
    VIEW3D_PT_modeling,
    VIEW3D_PT_setdress,
    VIEW3D_PT_copy_transforms
])
