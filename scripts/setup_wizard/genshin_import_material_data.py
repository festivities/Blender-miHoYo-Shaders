# Structure for class comes from a script initially written by Zekium from Discord
# Written by Mken from Discord

import bpy
import json
from pathlib import PurePosixPath

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, IntProperty, CollectionProperty
from bpy.types import Operator, PropertyGroup
import os

try:
    from scripts.setup_wizard.import_order import invoke_next_step
except Exception:
    print('Error! Run the first step of setup_wizard! Need to set up python script paths')


class GI_OT_GenshinImportMaterialData(Operator, ImportHelper):
    """Select Material Json Data Files"""
    bl_idname = "file.genshin_import_material_data"  # important since its how we chain file dialogs
    bl_label = "8_Genshin: Select Material Json Data Files"

    # ImportHelper mixin class uses this
    filename_ext = "*.*"

    import_path: StringProperty(
        name="Path",
        description="Path to the material json data files",
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
    files: CollectionProperty(type=PropertyGroup)

    local_material_mapping = {
        '_SpecMulti': 'Non-Metallic Specular Multiplier 1',
        '_SpecMulti2': 'Non-Metallic Specular Multiplier 2',
        '_SpecMulti3': 'Non-Metallic Specular Multiplier 3',
        '_SpecMulti4': 'Non-Metallic Specular Multiplier 4',
        '_SpecMulti5': 'Non-Metallic Specular Multiplier 5',
        '_Shininess': 'Non-Metallic Specular Shininess 1',
        '_Shininess2': 'Non-Metallic Specular Shininess 2',
        '_Shininess3': 'Non-Metallic Specular Shininess 3',
        '_Shininess4': 'Non-Metallic Specular Shininess 4',
        '_Shininess5': 'Non-Metallic Specular Shininess 5',
        '_MTMapLightColor': 'Metallic Light Color',
        '_MTMapDarkColor': 'Metallic Dark Color',
        '_MTShadowMultiColor': 'Metallic Shadow Multiply Color',
        '_MTMapTileScale': 'Metallic Map Tile Scale',
        '_MTMapBrightness': 'Metallic Brightness',
        '_MTSpecularColor': 'Metallic Specular Color',
        '_MTSpecularScale': 'Metallic Specular Scale',
        '_MTShininess': 'Metallic Specular Shininess',
        '_ShadowRampWidth': 'Ramp Width *NdotL only* *Ramp only*'
    }

    outline_mapping = {
        '_OutlineColor': 'Outline Color 1',
        '_OutlineColor2': 'Outline Color 2',
        '_OutlineColor3': 'Outline Color 3',
        '_OutlineColor4': 'Outline Color 4',
        '_OutlineColor5': 'Outline Color 5'
    }

    global_material_mapping = {
        '_MTUseSpecularRamp': 'Use Specular Ramp?',
        '_FaceBlushColor': 'Blush Color',
    }

    unsupported_body_parts = []

    # collei has dress on hair
    # ganyu has dress on body
    # yelan has dress1 on body and dress2 on hair

    # backwards compatibility for those who do not merge all objects to Body

    def execute(self, context):
        material_data_file_path = self.file_directory if self.file_directory else os.path.dirname(self.filepath)
        directory_file_path = os.path.dirname(self.filepath)

        for file in self.files:
            body_part = PurePosixPath(file.name).stem.split('_')[-1]

            if body_part in self.unsupported_body_parts:
                print(f'You imported a body part file: {file.name}, which was not expected in unsupported_body_parts: {self.unsupported_body_parts}')
                continue

            node_tree_group001_inputs = bpy.data.materials[f'miHoYo - Genshin {body_part}'].node_tree.nodes["Group.001"].inputs
            global_material_properties_node_inputs = bpy.data.node_groups["GLOBAL MATERIAL PROPERTIES"].nodes["Group Output"].inputs

            fp = open(f'{directory_file_path}/{file.name}')
            json_material_data = json.load(fp)

            if body_part != 'Face':
                for material_json_name, material_node_name in self.local_material_mapping.items():
                    material_json_value = self.__get_value_in_json(json_material_data, material_json_name)
                    material_node = node_tree_group001_inputs.get(self.local_material_mapping.get(material_json_name))

                    if not material_json_value:
                        continue

                    if type(material_node) is bpy.types.NodeSocketColor:
                        r = material_json_value['r']
                        g = material_json_value['g']
                        b = material_json_value['b']
                        a = material_json_value['a']
                        material_node.default_value = (r, g, b, a)
                    else:
                        material_node.default_value = material_json_value
                
                # Not sure, should we only apply Global Material Properties from Body .dat file?
                if body_part == 'Body':
                    for material_json_name, material_node_name in self.global_material_mapping.items():
                        material_json_value = self.__get_value_in_json(json_material_data, material_json_name)
                        material_node = global_material_properties_node_inputs.get(self.global_material_mapping.get(material_json_name))

                        if not material_json_value:
                            continue

                        if type(material_node) is bpy.types.NodeSocketColor:
                            r = material_json_value['r']
                            g = material_json_value['g']
                            b = material_json_value['b']
                            a = material_json_value['a']
                            material_node.default_value = (r, g, b, a)
                        else:
                            material_node.default_value = material_json_value
            self.setup_outline_colors(json_material_data, body_part)

        print('Imported materials...')
        invoke_next_step(self.next_step_idx)
        return {'FINISHED'}

    def setup_outline_colors(self, json_material_data, body_part):
        outlines_material = bpy.data.materials.get(f'miHoYo - Genshin {body_part} Outlines')
        outlines_shader_node_inputs = outlines_material.node_tree.nodes.get('Group.002').inputs

        for material_json_name, material_node_name in self.outline_mapping.items():
            material_json_value = self.__get_value_in_json(json_material_data, material_json_name)
            shader_node_input = outlines_shader_node_inputs.get(material_node_name)

            if not material_json_value:
                continue
            
            r = material_json_value['r']
            g = material_json_value['g']
            b = material_json_value['b']
            a = material_json_value['a']
            shader_node_input.default_value = (r, g, b, a)
    
    def __get_value_in_json(self, json_material_data, key):
        return json_material_data.get('m_SavedProperties').get('m_Floats').get(key) or \
            json_material_data.get('m_SavedProperties').get('m_Colors').get(key)


def register():
    bpy.utils.register_class(GI_OT_GenshinImportMaterialData)


def unregister():
    bpy.utils.unregister_class(GI_OT_GenshinImportMaterialData)


if __name__ == "__main__":
    register()