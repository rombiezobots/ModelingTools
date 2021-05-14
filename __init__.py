bl_info = {
    'name': 'Modeling Tools',
    'description': 'A few tools I\'ve written to facilitate modeling and setdress for productions in Blender.',
    'author': 'Sam Van Hulle',
    'version': (0, 0, 1),
    'blender': (2, 92, 0),
    'location': 'View3D > UI',
    'category': 'Tools'
}


##############################################################################
# Imports
##############################################################################


import bpy
from . import properties, operators, panels
modules = [properties, operators, panels]
from importlib import reload
for m in modules:
    reload(m)


##############################################################################
# Registration
##############################################################################


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()


if __name__ == '__main__':
    register()
