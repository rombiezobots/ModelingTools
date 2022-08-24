################################################################################
# Imports
################################################################################


if 'bpy' in locals():
    import importlib
    operators = importlib.reload(operators)
    properties = importlib.reload(properties)
    panels = importlib.reload(panels)

else:
    import bpy
    from . import properties
    from . import operators
    from . import panels


################################################################################
# Add-on information
################################################################################


bl_info = {
    'name': 'Modeling Tools',
    'description': 'A few tools I\'ve written to facilitate modeling and setdress for productions in Blender.',
    'author': 'Sam Van Hulle',
    'version': (0, 0, 3),
    'blender': (3, 3, 0),
    'location': 'View3D > UI',
    'category': 'Tools'
}


################################################################################
# Registration
################################################################################


modules = [
    properties,
    operators,
    panels,
]


def register():
    for mod in modules:
        mod.register()


def unregister():
    for mod in reversed(modules):
        mod.unregister()


if __name__ == '__main__':
    register()
