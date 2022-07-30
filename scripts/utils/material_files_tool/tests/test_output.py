import os
from pathlib import PurePath

main_py_file_path = os.path.dirname(os.path.dirname(__file__))
output_directory = f'{main_py_file_path}/output'
master_compare_directory_file_path = '<DirectoryWithTxtFilesGoesHere'


# Quick sanity check test, probably could've been written better, but this should do.
# Compares the material filenames (without their extensions) in the output and the "master_compare_directory"
def verify_no_file_discrepancy():
    character_folder_names = os.listdir(master_compare_directory_file_path)

    for character_folder_name in character_folder_names:
        master_material_files = os.listdir(f'{master_compare_directory_file_path}/{character_folder_name}/Material')
        output_material_files = os.listdir(f'{output_directory}/{character_folder_name}/Material')

        assert len(master_material_files) == len(output_material_files), f'{master_material_files} != {output_material_files}'
        
        for idx, master_material_file in enumerate(master_material_files):
            assert PurePath(master_material_file).stem == PurePath(output_material_files[idx]).stem, f'{master_material_file} != {output_material_files[idx]}'


if __name__ == '__main__':
    verify_no_file_discrepancy()
