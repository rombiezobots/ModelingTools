##############################################################################
# Imports
##############################################################################


import bpy


##############################################################################
# Classes
##############################################################################


class VIEW3D_PT_copy_transforms(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_copy_transforms'
    bl_label = 'Copy Transforms'
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'VIEW3D_PT_setdress'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        ct = context.scene.modeling_tools.setdress.copy_transforms
        lay = self.layout
        lay.use_property_split = True
        lay.use_property_decorate = False
        col = lay.column(align=True)
        row = col.split(factor=0.8)
        row.prop(ct, 'collection_from')
        row.label(
            text=f'({len(ct.collection_from.objects) if ct.collection_from else 0})')
        row = col.split(factor=0.8)
        row.prop(ct, 'collection_to')
        row.label(
            text=f'({len(ct.collection_to.objects) if ct.collection_to else 0})')
        lay.operator('modeling_tools.ct_copy_transforms', icon='PLAY')


##############################################################################
# Registration
##############################################################################


classes = [
    VIEW3D_PT_copy_transforms
]
