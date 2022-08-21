# Structure for file comes from a script initially written by Zekium from Discord
# Written by Mken from Discord
# Kudos to M4urlcl0 for bringing up adding the UV map (UV1) and 
# the armature bone settings when importing the FBX model

import bpy
import pathlib

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


class GI_OT_GenshinImportModel(Operator, ImportHelper):
    """Select the folder with the desired model to import"""
    bl_idname = "file.genshin_import_model"  # important since its how we chain file dialogs
    bl_label = "Genshin: Import Character Model - Select Character Model Folder"

    # ImportHelper mixin class uses this
    filename_ext = "*.*"

    import_path: StringProperty(
        name="Path",
        description="Path to the folder of the Model",
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
        character_model_folder_file_path = self.file_directory if self.file_directory else os.path.dirname(self.filepath)

        self.import_character_model(character_model_folder_file_path)
        self.reset_pose_location_and_rotation()

        # Quick-fix, just want to shove this in here for now...
        # Hide EffectMesh (gets deleted later on) and EyeStar
        # Now shoving in adding UV1 map too...
        for object in bpy.data.objects:
            if object.name == 'EffectMesh' or object.name == 'EyeStar':
                bpy.data.objects[object.name].hide_set(True)
            if object.type == 'MESH':  # I think this only matters for Body? But adding to all anyways
                object.data.uv_layers.new(name='UV1')

        invoke_next_step(self.next_step_idx, character_model_folder_file_path)
        return {'FINISHED'}

    def import_character_model(self, character_model_file_path_directory):
        character_model_file_path = self.__find_fbx_file(character_model_file_path_directory)
        bpy.ops.import_scene.fbx(
            filepath=character_model_file_path,
            force_connect_children=True,
            automatic_bone_orientation=True
        )
        self.report({'INFO'}, 'Imported character model...')
    
    def reset_pose_location_and_rotation(self):
        armature = [object for object in bpy.data.objects if object.type == 'ARMATURE'][0]  # expecting 1 armature
        bpy.context.view_layer.objects.active = armature

        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.loc_clear()
        bpy.ops.pose.rot_clear()
        bpy.ops.object.mode_set(mode='OBJECT')

    def __find_fbx_file(self, directory):
        for root, folder, files in os.walk(directory):
            for file_name in files:
                if '.fbx' in pathlib.Path(file_name).suffix:
                    return os.path.join(root, file_name)


def register():
    bpy.utils.register_class(GI_OT_GenshinImportModel)


def unregister():
    bpy.utils.unregister_class(GI_OT_GenshinImportModel)


if __name__ == "__main__":
    register()
