# Structure for class comes from a script initially written by Zekium from Discord
# Written by Mken from Discord

import bpy

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, IntProperty
from bpy.types import Operator
import os

# TOOD: Fix imports (requires you to at least do the first step in Import Wizard!)
import sys
if './scripts/streamlined_setup' not in sys.path:
    sys.path.append('./scripts/streamlined_setup')

from import_order import invoke_next_step


class GI_OT_GenshinImportOutlines(Operator, ImportHelper):
    """Select the `miHoYo - Outlines` to import Outlines"""
    bl_idname = "file.genshin_import_outlines"  # important since its how we chain file dialogs
    bl_label = "9_Genshin: Select with `miHoYo - Outlines`"

    # ImportHelper mixin class uses this
    filename_ext = "*.*"
    
    import_path: StringProperty(
        name = "Path",
        description = "Path to the folder containing the files to import",
        default = "",
        subtype = 'DIR_PATH'
        )

    filter_glob: StringProperty(
        default="*.*",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    next_step_idx: IntProperty()
    file_directory: StringProperty()

    def execute(self, context):
        if not bpy.data.node_groups.get('miHoYo - Outlines'):
            inner_path = 'NodeTree'
            object_name = 'miHoYo - Outlines'

            bpy.ops.wm.append(
                filepath=os.path.join(self.filepath, inner_path, object_name),
                directory=os.path.join(self.filepath, inner_path),
                filename=object_name
            )
        invoke_next_step(self.next_step_idx)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(GI_OT_GenshinImportOutlines)


def unregister():
    bpy.utils.unregister_class(GI_OT_GenshinImportOutlines)


if __name__ == "__main__":
    register()