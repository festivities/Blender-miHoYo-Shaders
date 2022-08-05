# Structure for file comes from a script initially written by Zekium from Discord
# Written by Mken from Discord

import bpy
import pathlib

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


class GI_OT_GenshinImportOutlineLightmaps(Operator, ImportHelper):
    """Select the folder with the lightmaps to import"""
    bl_idname = "file.genshin_import_outline_lightmaps"  # important since its how we chain file dialogs
    bl_label = "7_Genshin: Select Import Outline Lightmaps"

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

    # TODO: Seriously need to centralize this into one file...
    material_assignment_mapping = {
        'Yelan': {
            'miHoYo - Genshin Dress1': 'Body',
            'miHoYo - Genshin Dress2': 'Hair'
        },
        'Collei': {
            'miHoYo - Genshin Dress': 'Hair'
        },
        'Ganyu': {
            'miHoYo - Genshin Dress': 'Body'
        },
        'Rosaria': {
            'miHoYo - Genshin Dress1': 'Hair',
            'miHoYo - Genshin Dress2': 'Body'
        }
    }

    def execute(self, context):
        character_model_folder_file_path = self.file_directory if self.file_directory else os.path.dirname(self.filepath)
        character_name = ''
        
        for name, folder, files in os.walk(character_model_folder_file_path):
            lightmap_files = [file for file in files if 'Lightmap' in file]
        

            for tmp_character_name in self.material_assignment_mapping.keys():
                for file in files:
                    if tmp_character_name in file:
                        character_name = tmp_character_name
                        break
            character_material_mapping = self.material_assignment_mapping.get(character_name)
            outline_materials = [material for material in bpy.data.materials.values() if 'Outlines' in material.name and material.name != 'miHoYo - Genshin Outlines']

            for outline_material in outline_materials:
                original_material_name = outline_material.name.strip(' Outlines')
                material_part_name = character_material_mapping.get(original_material_name) if character_material_mapping else ''
                # print(f'original: {original_material_name}')
                # print(f'material: {material_part_name}')
                material_part_name_lightmap = material_part_name
                if not material_part_name:
                    material_part_name = outline_material.name.split(' ')[-2]
                    material_part_name_lightmap = 'Body' if material_part_name == 'Dress' else \
                        material_part_name

                if material_part_name != 'Face':
                    print(material_part_name_lightmap)
                    print(lightmap_files)

                    file = [file for file in lightmap_files if material_part_name_lightmap in file][0]

                    img_path = character_model_folder_file_path + "/" + file
                    img = bpy.data.images.load(filepath = img_path, check_existing=True)
                    img.alpha_mode = 'CHANNEL_PACKED'

                    bpy.data.materials.get(f'miHoYo - Genshin {material_part_name} Outlines').node_tree.nodes.get('Image Texture').image = img

        invoke_next_step(self.next_step_idx, character_model_folder_file_path)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(GI_OT_GenshinImportOutlineLightmaps)


def unregister():
    bpy.utils.unregister_class(GI_OT_GenshinImportOutlineLightmaps)


if __name__ == "__main__":
    register()
