##############################################################################
# Imports
##############################################################################


import bpy


##############################################################################
# Classes
##############################################################################


class WrapperObject(bpy.types.PropertyGroup):

    obj_name: bpy.props.StringProperty()

class CopyTransformsProperties(bpy.types.PropertyGroup):

    rotation_or_face_normals: bpy.props.EnumProperty(name='Rotation', items=[
        ('use_transforms', 'Use Object Rotation',
            'Use the objects\' transform values'),
        ('use_face_normals', 'Use First Face Normal',
            'Use the normal of the first face found in each object (Y-up)')
    ])
    set_a: bpy.props.CollectionProperty(type=WrapperObject)
    set_b: bpy.props.CollectionProperty(type=WrapperObject)

class ModelingToolsSceneProperties(bpy.types.PropertyGroup):

    copy_transforms: bpy.props.PointerProperty(type=CopyTransformsProperties)

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
        lay.operator('modeling_tools.modeling_ot_subdiv_keep_corners',
            icon='MOD_SUBSURF')
        lay.operator('modeling_tools.modeling_ot_select_unsubdivided',
            icon='MOD_SUBSURF')
        lay.operator('modeling_tools.modeling_ot_origin_to_bottom_center',
            icon='OBJECT_ORIGIN')

class VIEW3D_PT_setdress(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_setdress'
    bl_label = 'Setdress'
    bl_parent_id = 'VIEW3D_PT_modeling_tools'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        lay = self.layout
        lay.scale_y = 1.5
        col = lay.column(align=True)
        col.operator('modeling_tools.setdress_ot_minimize_empties',
            icon='OUTLINER_OB_EMPTY')
        col.operator('modeling_tools.setdress_ot_set_collection_instance_offset',
            icon='OUTLINER_OB_EMPTY')
        col.operator('modeling_tools.setdress_ot_snap_rotation',
            icon='CON_ROTLIMIT')

class VIEW3D_PT_copy_transforms(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_copy_transforms'
    bl_label = 'Copy Transforms'
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'VIEW3D_PT_modeling_tools'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        set_a = context.scene.modeling_tools.copy_transforms.set_a
        set_b = context.scene.modeling_tools.copy_transforms.set_b
        lay = self.layout
        row = lay.row(align=True)
        row.scale_y = 1.5
        row.operator('modeling_tools.ct_ot_clear_tt_set', icon='X',
            text='').tt_set='a'
        row.operator('modeling_tools.ct_ot_selection_to_tt_set',
            text=f'From {len(set_a)}').tt_set='a'
        row.operator('modeling_tools.ct_ot_copy_transforms',
            icon='FORWARD', text='')
        row.operator('modeling_tools.ct_ot_selection_to_tt_set',
            text=f'To {len(set_b)}').tt_set='b'
        row.operator('modeling_tools.ct_ot_clear_tt_set', icon='X',
            text='').tt_set='b'
        lay.prop(context.scene.modeling_tools.copy_transforms,
            'rotation_or_face_normals')
        lay.operator('modeling_tools.ct_ot_delete_original_objects',
            icon='TRASH')


##############################################################################
# Registration
##############################################################################


classes = [
    WrapperObject,
    CopyTransformsProperties,
    ModelingToolsSceneProperties,
    VIEW3D_PT_modeling_tools,
    VIEW3D_PT_modeling,
    VIEW3D_PT_setdress,
    VIEW3D_PT_copy_transforms,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.modeling_tools = bpy.props.PointerProperty(
        type=ModelingToolsSceneProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

