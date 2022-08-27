##############################################################################
# Imports
##############################################################################


import bpy


##############################################################################
# Classes
##############################################################################


class CT_OT_copy_transforms(bpy.types.Operator):
    '''Copy transformation values from a collection of objects to another'''

    bl_idname = 'modeling_tools.ct_copy_transforms'
    bl_label = 'Copy Transforms'
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        ct = context.scene.modeling_tools.setdress.copy_transforms
        return len(ct.collection_from.objects) == len(ct.collection_to.objects)

    def execute(self, context):
        ct = context.scene.modeling_tools.setdress.copy_transforms
        for index, ob_to in enumerate(ct.collection_to.objects):
            ob_from = ct.collection_from.objects[index]
            ob_to.location = ob_from.location
            ob_to.rotation_euler = ob_from.rotation_euler
            ob_to.scale = ob_from.scale
        return {'FINISHED'}


##############################################################################
# Registration
##############################################################################


classes = [
    CT_OT_copy_transforms,
]
