# Structure for file comes from a script initially written by Zekium from Discord
# Written by Mken from Discord

import bpy
import pathlib

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, IntProperty, BoolProperty, EnumProperty
from bpy.types import Operator
import os

# TOOD: Fix imports (requires you to at least do the first step in Import Wizard!)
import sys
if './scripts/streamlined_setup' not in sys.path:
    sys.path.append('./scripts/streamlined_setup')

from import_order import invoke_next_step

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


class GI_OT_GenshinImportModel(Operator, ImportHelper):
    """Select the folder with the desired model to import"""
    bl_idname = "file.genshin_import_model"  # important since its how we chain file dialogs
    bl_label = "2_Genshin: Select Model Folder"

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

        character_name = ''
        for name, folder, files in os.walk(character_model_folder_file_path):
            for file in files:
                for tmp_character_name in material_assignment_mapping.keys():
                    if tmp_character_name in file:
                        character_name = tmp_character_name

        self.__import_character_model(character_model_folder_file_path)
        self.__join_body_parts_to_body()
        self.__replace_default_materials_with_genshin_materials(character_name)

        invoke_next_step(self.next_step_idx, character_model_folder_file_path)
        return {'FINISHED'}

    def __import_character_model(self, character_model_file_path_directory):
        character_model_file_path = self.__find_fbx_file(character_model_file_path_directory)
        bpy.ops.import_scene.fbx(filepath=character_model_file_path)
        print('Imported character model...')

    def __find_fbx_file(self, directory):
        for root, folder, files in os.walk(directory):
            for file_name in files:
                if '.fbx' in pathlib.Path(file_name).suffix:
                    return os.path.join(root, file_name)
    
    def __join_body_parts_to_body(self):
        character_model = None
        for object in bpy.context.scene.objects:
            if object.type == 'ARMATURE':
                character_model = object
                continue

        character_model_body = [body_part for body_part in character_model.children if body_part.name == 'Body'][0]
        character_model_children_without_body = [body_part for body_part in character_model.children if body_part.name != 'Body']
        
        for character_model_child in character_model_children_without_body:
            character_model_child.select_set(True)
        bpy.context.view_layer.objects.active = character_model_body
        bpy.ops.object.join()
    
    def __replace_default_materials_with_genshin_materials(self, character_name):
        # TODO: We actually are specifically looking at meshes here...impacts unjoined workflows
        body_mesh_object = [object for object in bpy.context.scene.objects if object.type == 'MESH'][0]

        for material_slot in body_mesh_object.material_slots:
            material_name = material_slot.name
            mesh_body_part_name = material_name.split('_')[-1]
            genshin_material = bpy.data.materials.get(f'miHoYo - Genshin {mesh_body_part_name}')

            if genshin_material:            
                material_slot.material = genshin_material
            elif 'Dress' in mesh_body_part_name:
                material_mapping = material_assignment_mapping.get(character_name)
                print(material_mapping)
                body_part = material_mapping.get(f'miHoYo - Genshin {mesh_body_part_name}')

                genshin_material = self.__clone_material_and_rename(material_slot, f'miHoYo - Genshin {body_part}', mesh_body_part_name)
            elif material_name == 'miHoYoDiffuse':
                material_slot.material = bpy.data.materials.get(f'miHoYo - Genshin Body')
                continue
            else:
                print(f'Ignoring unknown mesh body part in character model: {mesh_body_part_name}')
                continue

            genshin_main_shader_node = genshin_material.node_tree.nodes.get('Group.001')
            genshin_main_shader_node.node_tree = self.__clone_shader_node_and_rename(genshin_material, mesh_body_part_name)
        print('Replaced default materials with Genshin shader materials...')
    
    def __clone_material_and_rename(self, material_slot, mesh_body_part_name_template, mesh_body_part_name):
        new_material = bpy.data.materials.get(mesh_body_part_name_template).copy()
        new_material.name = f'miHoYo - Genshin {mesh_body_part_name}'

        material_slot.material = new_material
        return new_material

    def __clone_shader_node_and_rename(self, material, mesh_body_part_name):
        new_shader_node_tree = material.node_tree.nodes.get('Group.001').node_tree.copy()
        new_shader_node_tree.name = f'miHoYo - Genshin {mesh_body_part_name}'
        return new_shader_node_tree


def register():
    bpy.utils.register_class(GI_OT_GenshinImportModel)


def unregister():
    bpy.utils.unregister_class(GI_OT_GenshinImportModel)


if __name__ == "__main__":
    register()
