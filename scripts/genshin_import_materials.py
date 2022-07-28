# Structure for file comes from a script initially written by Zekium from Discord
# Written by Mken from Discord

import bpy

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
import os

import sys
if './scripts' not in sys.path:
    sys.path.append('./scripts')

from genshin_import_character_model import GI_OT_GenshinImportModel


class GI_OT_GenshinImportMaterials(Operator, ImportHelper):
    """Select Festivity's Shaders folder to import materials"""
    bl_idname = "file.genshin_import_materials"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Genshin: Import Festivity Folder"

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
        BLEND_FILE_WITH_GENSHIN_MATERIALS = 'miHoYo - Genshin Impact.blend'
        MATERIAL_PATH_INSIDE_BLEND_FILE = 'Material'

        DIRECTORY_WITH_BLEND_FILE_PATH = os.path.join(
            FILEPATH_DIRECTORY,
            BLEND_FILE_WITH_GENSHIN_MATERIALS,
            MATERIAL_PATH_INSIDE_BLEND_FILE
        )
        NAMES_OF_GENSHIN_MATERIALS = [
            {'name': 'miHoYo - Genshin Body'},
            {'name': 'miHoYo - Genshin Face'},
            {'name': 'miHoYo - Genshin Hair'},
            {'name': 'miHoYo - Genshin Outlines'}
        ]

        bpy.ops.wm.append(
            directory=DIRECTORY_WITH_BLEND_FILE_PATH,
            files=NAMES_OF_GENSHIN_MATERIALS
        )

        bpy.ops.file.genshin_import_model('INVOKE_DEFAULT')

        return {'FINISHED'}


def register():
    bpy.utils.register_class(GI_OT_GenshinImportMaterials)

    # Originally I tried checking, but this way is less bug-prone and is more Pythonic
    # Tried checking for attributes (on bpy.ops.file.xxx), but it seemed to always return true
    try:
        bpy.utils.register_class(GI_OT_GenshinImportModel)
    except ValueError:
        pass  # expected if class is already registered


def unregister():
    bpy.utils.unregister_class(GI_OT_GenshinImportMaterials)
    bpy.utils.unregister_class(GI_OT_GenshinImportModel)


if __name__ == "__main__":
    register()
