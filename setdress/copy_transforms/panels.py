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
        setdress = context.scene.modeling_tools.setdress
        batch_from = setdress.copy_transforms.batch_from
        batch_to = setdress.copy_transforms.batch_to
        lay = self.layout
        row = lay.row(align=True)
        row.scale_y = 1.5
        row.operator('modeling_tools.ct_ot_clear_batch', icon='X',
                     text='').batch = 'a'
        row.operator('modeling_tools.ct_ot_selection_to_batch',
                     text=f'From {len(batch_from)}').batch = 'a'
        row.operator('modeling_tools.ct_ot_copy_transforms',
                     icon='FORWARD', text='')
        row.operator('modeling_tools.ct_ot_selection_to_batch',
                     text=f'To {len(batch_to)}').batch = 'b'
        row.operator('modeling_tools.ct_ot_clear_batch', icon='X',
                     text='').batch = 'b'
        lay.prop(setdress.copy_transforms,
                 'rotation_or_face_normals')
        lay.operator('modeling_tools.ct_ot_delete_original_objects',
                     icon='TRASH')


##############################################################################
# Registration
##############################################################################


classes = [
    VIEW3D_PT_copy_transforms
]
