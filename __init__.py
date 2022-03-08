


################################################################################
# Imports
################################################################################


if 'bpy' in locals():
    import importlib
    operators = importlib.reload(operators)
    ui = importlib.reload(ui)

else:
    import bpy
    from . import operators
    from . import ui


################################################################################
# Add-on information
################################################################################


bl_info = {
    'name': 'Modeling Tools',
    'description': 'A few tools I\'ve written to facilitate modeling and setdress for productions in Blender.',
    'author': 'Sam Van Hulle',
    'version': (0, 0, 1),
    'blender': (2, 92, 0),
    'location': 'View3D > UI',
    'category': 'Tools'
}


################################################################################
# Registration
################################################################################


modules = [
    operators,
    ui
]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in reversed(modules):
        module.unregister()

if __name__ == '__main__':
    register()
