# Structure for file comes from a script initially written by Zekium from Discord
# Written by Mken from Discord

import bpy
import json

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


class GI_OT_GenshinReplaceDefaultMaterials(Operator, ImportHelper):
    """Select the folder with the desired model to import"""
    bl_idname = "file.genshin_replace_default_materials"  # important since its how we chain file dialogs
    bl_label = "Genshin: Replace Default Materials - Select Character Model Folder"

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

    character_material_mapping_file = open('scripts/setup_wizard/character_material_mapping.json')
    material_assignment_mapping = json.load(character_material_mapping_file)

    def execute(self, context):
        character_model_folder_file_path = self.file_directory if self.file_directory else os.path.dirname(self.filepath)

        character_name = ''
        for name, folder, files in os.walk(character_model_folder_file_path):
            for file in files:
                for tmp_character_name in self.material_assignment_mapping.keys():
                    if tmp_character_name in file:
                        character_name = tmp_character_name
                        break
            break

        self.replace_default_materials_with_genshin_materials(character_name)

        invoke_next_step(self.next_step_idx, character_model_folder_file_path)
        return {'FINISHED'}
    
    def replace_default_materials_with_genshin_materials(self, character_name):
        meshes = [mesh for mesh in bpy.context.scene.objects if mesh.type == 'MESH']

        for mesh in meshes:
            for material_slot in mesh.material_slots:
                material_name = material_slot.name
                mesh_body_part_name = material_name.split('_')[-1]
                genshin_material = bpy.data.materials.get(f'miHoYo - Genshin {mesh_body_part_name}')

                if genshin_material:            
                    material_slot.material = genshin_material
                elif 'Dress' in mesh_body_part_name:
                    self.report({'INFO'}, 'Dress detected on character model!')
                    material_mapping = self.material_assignment_mapping.get(character_name)

                    if material_mapping:
                        body_part = material_mapping.get(f'miHoYo - Genshin {mesh_body_part_name}')
                        genshin_material = self.__clone_material_and_rename(material_slot, f'miHoYo - Genshin {body_part}', mesh_body_part_name)
                    else:
                        genshin_material = self.__clone_material_and_rename(material_slot, f'miHoYo - Genshin Body', mesh_body_part_name)
                elif material_name == 'miHoYoDiffuse':
                    material_slot.material = bpy.data.materials.get(f'miHoYo - Genshin Body')
                    continue
                else:
                    self.report({'WARNING'}, f'Ignoring unknown mesh body part in character model: {mesh_body_part_name}')
                    continue

                # Don't need to duplicate multiple Face shader nodes
                if genshin_material.name != f'miHoYo - Genshin Face':
                    genshin_main_shader_node = genshin_material.node_tree.nodes.get('Group.001')
                    genshin_main_shader_node.node_tree = self.__clone_shader_node_and_rename(genshin_material, mesh_body_part_name)
        self.report({'INFO'}, 'Replaced default materials with Genshin shader materials...')
    
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
    bpy.utils.register_class(GI_OT_GenshinReplaceDefaultMaterials)


def unregister():
    bpy.utils.unregister_class(GI_OT_GenshinReplaceDefaultMaterials)


if __name__ == "__main__":
    register()
