# Written by Mken from Discord

import bpy
import json

try:
    from join_body_parts_to_body import join_body_parts_to_body
except:
    pass

FESTIVITY_ROOT_FOLDER_FILE_PATH = 'FESTIVITY_ROOT_FOLDER_FILE_PATH'
CHARACTER_MODEL_FOLDER_FILE_PATH = 'character_model_folder_file_path'
COMPONENT_NAME = 'component_name'
BL_IDNAME_FUNCTION = 'function_to_call'
ENABLED = 'enabled'
CACHE_KEY = 'cache_key'

module_path_to_streamlined_setup = ''

cache = {
    FESTIVITY_ROOT_FOLDER_FILE_PATH: '',
    CHARACTER_MODEL_FOLDER_FILE_PATH: ''
}


def invoke_next_step(current_step_idx: int, file_path_to_cache=None, path_to_streamlined_setup=''):
    if path_to_streamlined_setup:
        global module_path_to_streamlined_setup
        module_path_to_streamlined_setup = path_to_streamlined_setup

    # We use a config.json so that we can make changes without having to restart Blender
    # TODO: Make this a class that gets instantiated in each component? 
    # TOOD: Making a class may allow us to move config.json data back into this module?
    file = open(f'{module_path_to_streamlined_setup}/config.json')
    config = json.load(file)


    if current_step_idx <= 0 or current_step_idx > len(config):
        return
    # Disabled cache, it does not work as intended b/c it carries over from past usage
    # if file_path_to_cache is not None and config[current_step_idx][CACHE_KEY]:
    #     cache_file_path(config, current_step_idx - 1, file_path_to_cache)
    
    if config[str(current_step_idx)][ENABLED]:
        cached_file_directory = cache.get(config[str(current_step_idx)][CACHE_KEY], '')
        execute_or_invoke = 'EXEC' if cached_file_directory else 'INVOKE'
        component_name = config[str(current_step_idx)][COMPONENT_NAME]
        function_to_use = ComponentFunctionFactory.create_component_function(component_name)

        if type(function_to_use) is bpy.ops._BPyOpsSubModOp:
            print(f'Calling {function_to_use} with {execute_or_invoke}_DEFAULT w/ cache: {cached_file_directory}')
            function_to_use(
                    f'{execute_or_invoke}_DEFAULT', 
                    next_step_idx=current_step_idx + 1, 
                    file_directory=cached_file_directory
            )
        else:
            function_to_use(current_step_idx + 1)
    else:
        invoke_next_step(current_step_idx + 1)


def cache_file_path(config, last_step_idx, file_path_to_cache):
    step = config[str(last_step_idx)]
    step_cache_key = step.get(CACHE_KEY)

    print(f'Assigning `{step_cache_key}:{file_path_to_cache}` in cache')
    cache[step_cache_key] = file_path_to_cache


class ComponentFunctionFactory:
    @staticmethod
    def create_component_function(component_name):
        if component_name == 'import_materials':
            return bpy.ops.file.genshin_import_materials
        elif component_name == 'join_body_parts_to_body':
            return join_body_parts_to_body
        elif component_name == 'import_character_model':
            return bpy.ops.file.genshin_import_model
        elif component_name == 'import_character_textures':
            return bpy.ops.file.genshin_import_textures
        elif component_name == 'import_material_data':
            return bpy.ops.file.genshin_import_material_data
        else:
            raise Exception(f'Unknown component name passed into {__name__}: {component_name}')