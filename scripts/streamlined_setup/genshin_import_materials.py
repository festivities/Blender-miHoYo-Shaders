# Structure for file comes from a script initially written by Zekium from Discord
# Written by Mken from Discord

from enum import Enum
import bpy

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, IntProperty, BoolProperty, EnumProperty
from bpy.types import Operator
import os

import sys
if './scripts/streamlined_setup' not in sys.path:
    sys.path.append('./scripts/streamlined_setup')

from import_order import invoke_next_step


class GI_OT_GenshinImportMaterials(Operator, ImportHelper):
    """Select Festivity's Shaders folder to import materials"""
    bl_idname = "file.genshin_import_materials"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "1_Genshin: Select Festivity Folder"

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

    next_step_idx: IntProperty()
    file_directory: StringProperty()

    def execute(self, context):
        BLEND_FILE_WITH_GENSHIN_MATERIALS = 'miHoYo - Genshin Impact.blend'
        MATERIAL_PATH_INSIDE_BLEND_FILE = 'Material'
        project_root_directory_file_path = self.file_directory if self.file_directory else os.path.dirname(self.filepath)

        DIRECTORY_WITH_BLEND_FILE_PATH = os.path.join(
            project_root_directory_file_path,
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

        print('Imported materials...')
        invoke_next_step(self.next_step_idx, project_root_directory_file_path)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(GI_OT_GenshinImportMaterials)


def unregister():
    bpy.utils.unregister_class(GI_OT_GenshinImportMaterials)


if __name__ == "__main__":
    register()
