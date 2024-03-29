##############################################################################
# Imports
##############################################################################


if 'bpy' in locals():
    import importlib
    modeling = importlib.reload(modeling)
    setdress = importlib.reload(setdress)
else:
    import bpy
    from .modeling import operators as modeling
    from .setdress import operators as setdress


##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory(
    modeling.classes + setdress.classes
)
