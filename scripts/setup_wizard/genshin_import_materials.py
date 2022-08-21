# Structure for file comes from a script initially written by Zekium from Discord
# Written by Mken from Discord

import bpy

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, IntProperty
from bpy.types import Operator
import os

try:
    from scripts.setup_wizard.import_order import invoke_next_step
except Exception:
    print('Error! Run the first step of setup_wizard! Need to set up python script paths')

BLEND_FILE_WITH_GENSHIN_MATERIALS = 'miHoYo - Genshin Impact.blend'
MATERIAL_PATH_INSIDE_BLEND_FILE = 'Material'

NAMES_OF_GENSHIN_MATERIALS = [
    {'name': 'miHoYo - Genshin Body'},
    {'name': 'miHoYo - Genshin Face'},
    {'name': 'miHoYo - Genshin Hair'},
    {'name': 'miHoYo - Genshin Outlines'}
]


class GI_OT_GenshinImportMaterials(Operator, ImportHelper):
    """Select Festivity's Shaders folder to import materials"""
    bl_idname = "file.genshin_import_materials"  # important since its how we chain file dialogs
    bl_label = "Genshin: Import Materials - Select Festivity's Shaders Folder"

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
        project_root_directory_file_path = self.file_directory if self.file_directory else os.path.dirname(self.filepath)
        directory_with_blend_file_path = os.path.join(
            project_root_directory_file_path,
            BLEND_FILE_WITH_GENSHIN_MATERIALS,
            MATERIAL_PATH_INSIDE_BLEND_FILE
        )

        bpy.ops.wm.append(
            directory=directory_with_blend_file_path,
            files=NAMES_OF_GENSHIN_MATERIALS
        )

        self.report({'INFO'}, 'Imported Shader/Genshin Materials...')
        invoke_next_step(self.next_step_idx, project_root_directory_file_path)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(GI_OT_GenshinImportMaterials)


def unregister():
    bpy.utils.unregister_class(GI_OT_GenshinImportMaterials)


if __name__ == "__main__":
    register()
