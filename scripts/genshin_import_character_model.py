# Converted from a script initially written by Zekium from Discord
# Written by Mken
# WIP - Test Class for multiple file explorer dialogs

import bpy

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
import os


class GI_OT_GenshinImportMaterialsTest(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "file.genshin_import_materials_test"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Genshin: Import MaterialsTest"

    # ImportHelper mixin class uses this
    filename_ext = "*.*"

    import_path: StringProperty(
        name="Path",
        description="Path to the folder of Festivity's Shaders project",
        default="",
        subtype='DIR_PATH'
    )

    filter_glob: StringProperty(
        default="*.*",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        FILEPATH_DIRECTORY = os.path.dirname(self.filepath)
        print('do stuff')
        return {'FINISHED'}


def register():
    bpy.utils.register_class(GI_OT_GenshinImportMaterialsTest)


def unregister():
    bpy.utils.unregister_class(GI_OT_GenshinImportMaterialsTest)


if __name__ == "__main__":
    register()
