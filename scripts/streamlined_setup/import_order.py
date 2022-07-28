# Written by Mken from Discord

import bpy

FESTIVITY_ROOT_FOLDER_FILE_PATH = 'FESTIVITY_ROOT_FOLDER_FILE_PATH'
CHARACTER_MODEL_FOLDER_FILE_PATH = 'CHARACTER_MODEL_FOLDER_FILE_PATH'
BL_IDNAME_FUNCTION = 'function_to_call'
CACHE_KEY = 'cache'

cache = {
    FESTIVITY_ROOT_FOLDER_FILE_PATH: '',
    CHARACTER_MODEL_FOLDER_FILE_PATH: ''
}

steps = {
    1: { BL_IDNAME_FUNCTION: bpy.ops.file.genshin_import_materials, CACHE_KEY: '' },
    2: { BL_IDNAME_FUNCTION: bpy.ops.file.genshin_import_model, CACHE_KEY: '' },
    3: { BL_IDNAME_FUNCTION: bpy.ops.file.genshin_import_textures, CACHE_KEY: CHARACTER_MODEL_FOLDER_FILE_PATH },
}


def invoke_next_step(current_step_idx: int, file_path_to_cache=None):
    if current_step_idx == 0 or current_step_idx > len(steps):
        return
    if file_path_to_cache is not None:
        cache_file_path(current_step_idx - 1, file_path_to_cache)

    execute_or_invoke = 'EXEC' if steps[current_step_idx][CACHE_KEY] else 'INVOKE'
    cached_file_directory = cache.get(steps[current_step_idx][CACHE_KEY], '')
    function_to_use = steps[current_step_idx][BL_IDNAME_FUNCTION]

    print(f'Calling {function_to_use} with {execute_or_invoke}_DEFAULT')
    function_to_use(
            f'{execute_or_invoke}_DEFAULT', 
            next_step_idx=current_step_idx + 1, 
            file_directory=cached_file_directory
    )


def cache_file_path(last_step_idx, file_path_to_cache):
    if steps[last_step_idx][BL_IDNAME_FUNCTION] == steps[1][BL_IDNAME_FUNCTION]:
        cache[FESTIVITY_ROOT_FOLDER_FILE_PATH] = file_path_to_cache
    elif steps[last_step_idx][BL_IDNAME_FUNCTION] == steps[2][BL_IDNAME_FUNCTION] or steps[last_step_idx] == steps[3][BL_IDNAME_FUNCTION]:
        cache[CHARACTER_MODEL_FOLDER_FILE_PATH] = file_path_to_cache
