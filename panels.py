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
        

##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory([
    VIEW3D_PT_modeling_tools,
    VIEW3D_PT_modeling,
    VIEW3D_PT_setdress
])
