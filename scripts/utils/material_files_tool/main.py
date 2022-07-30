import errno
import io
import json
import os
import UnityPy

main_py_file_path = os.path.dirname(os.path.realpath(__file__))
output_directory = f'{main_py_file_path}/output'


def main():
    print('Please input the file path to the assets file')
    assets_file_path = input('Example: G:\Some Folder\shardassets1.assets\n\n')
    print('\n')

    print('Please input the file path to the base folder with all the characters (which have .dat files in sub-folders)')
    print('Expecting inside folder structure to be like: {BaseFolder}/{CharacterName}/Material/{.dat files}')
    dat_files_folder_path = input('Example: G:\Some Folder\Playable Character Materials 2.8\n\n')
    print('\n')

    for character_folder in os.listdir(dat_files_folder_path):
        material_dat_folder = f'{dat_files_folder_path}/{character_folder}/Material' 
        dat_files = os.listdir(material_dat_folder)
        unique_dat_file_paths = [f'{material_dat_folder}/{dat_file_name}' for dat_file_name in dat_files \
            if '_Mat' in dat_file_name and 
            'Avatar_' in dat_file_name and
            'TT' not in dat_file_name and
            '#' not in dat_file_name and
            'Effect' not in dat_file_name
        ]  # I really do not like this, but it's adequate for now.
    
        assets_env = UnityPy.load(assets_file_path)
        material_object_idx = -1

        for idx, assets_object in enumerate(assets_env.objects):
            if assets_object.type.name == 'Material':
                material_object_idx = idx
                break

        for dat_file_path in unique_dat_file_paths:
            dat_file_env = UnityPy.load(dat_file_path)
            dat_file_bytes = dat_file_env.file.bytes

            assets_material_object = assets_env.objects[material_object_idx]
            assets_material_data = assets_material_object.read()

            assets_material_data.set_raw_data(dat_file_bytes)
            assets_material_data.save()

            patched_material = io.BytesIO(assets_env.file.save())
            patched_value_env = UnityPy.load(patched_material)

            json_data = json.dumps(
                patched_value_env.objects[material_object_idx].read_typetree(),
                indent=4,
                ensure_ascii=False
            ).encode('utf-8')

            file_name = patched_value_env.objects[material_object_idx].read().name
            character_output_directory = f'{output_directory}/{character_folder}'

            try:
                os.makedirs(f'{character_output_directory}/Material')
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
                pass

            with open(f'{character_output_directory}/Material/{file_name}.json', 'wb') as f:
                print(f'Writing ".../output/{character_folder}/Material/{file_name}.json"')
                f.write(json_data)
    
    print('Done!')


if __name__ == '__main__':
    main()
