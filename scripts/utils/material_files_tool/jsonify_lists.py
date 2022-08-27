# The Playable Character Materials json have data stored in arrays.
# It would be easier to have these stored in dicts instead.
# This file will process the arrays and turn them into dicts

import errno
import json
import os

SAVED_PROPERTIES_FIELD = 'm_SavedProperties'

main_py_file_path = os.path.dirname(os.path.realpath(__file__))
output_directory = f'{main_py_file_path}/output'
modified_output_directory = f'{main_py_file_path}/modified_output'


def jsonify_saved_properties_field():
    character_folder_names = os.listdir(output_directory)

    for character_folder_name in character_folder_names:
        character_material_files = os.listdir(f'{output_directory}/{character_folder_name}/Material')
        character_material_files_file_path = f'{output_directory}/{character_folder_name}/Material'
        modified_character_material_files_file_path = f'{modified_output_directory}/{character_folder_name}/Material'

        for character_material_file in character_material_files:
            fp = open(f'{character_material_files_file_path}/{character_material_file}')
            data = json.load(fp)

            m_savedProperties_dict = data.get(SAVED_PROPERTIES_FIELD)
            new_m_savedProperties_dict = {}

            for key, values in m_savedProperties_dict.items():
                if type(values) is list:
                    tmp_m_value_dict = {}
                    for value in values:
                        new_dict = {value[idx]: value[idx + 1] for idx in range(0, len(value), 2)}
                        tmp_m_value_dict = {**tmp_m_value_dict, **new_dict}  # adds/merges the new dict
                    new_m_savedProperties_dict[key] = tmp_m_value_dict
                else: 
                    print(f'Unexpected type: {type(values)}')
            
            data[SAVED_PROPERTIES_FIELD] = new_m_savedProperties_dict
            json_data_to_export = json.dumps(
                data,
                indent=4,
                ensure_ascii=False
            ).encode('utf-8')

            character_output_directory = f'{modified_output_directory}/{character_folder_name}'

            try:
                os.makedirs(f'{character_output_directory}/Material')
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
                pass

            with open(f'{modified_character_material_files_file_path}/{character_material_file}', 'wb') as f:
                print(f'Writing ".../modified_output/{character_folder_name}/Material/{character_material_file}"')
                f.write(json_data_to_export)
    
    print('Done writing modified jsons')


if __name__ == '__main__':
    jsonify_saved_properties_field()