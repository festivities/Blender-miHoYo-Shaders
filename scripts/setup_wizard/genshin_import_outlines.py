# Structure for class comes from a script initially written by Zekium from Discord
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


class GI_OT_GenshinImportOutlines(Operator, ImportHelper):
    """Select the `miHoYo - Outlines` to import Outlines"""
    bl_idname = "file.genshin_import_outlines"  # important since its how we chain file dialogs
    bl_label = "Genshin: Select with `miHoYo - Outlines`"

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