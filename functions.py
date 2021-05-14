##############################################################################
# Imports
##############################################################################


import bpy


##############################################################################
# Functions
##############################################################################


def is_datablock_linked(datablock:bpy.types.ID) -> bool:
    return datablock.library or datablock.override_library


def select_unsubdivided():
    objects = [ob for ob in bpy.context.scene.objects if ob.type == 'MESH' and not is_datablock_linked(ob)]
    bpy.ops.object.select_all(action = 'DESELECT')
    for ob in objects:
        has_enabled_subsurf_modifiers = False
        for mod in ob.modifiers:
            if mod.type == 'SUBSURF':
                has_enabled_subsurf_modifiers = mod.show_render and (mod.render_levels > 0 or ob.cycles.use_adaptive_subdivision)
                break
        if ob.name in bpy.context.view_layer.objects:
            ob.select_set(not has_enabled_subsurf_modifiers)