# Written by Mken from Discord

import bpy

try:
    from join_body_parts_to_body import join_body_parts_to_body
except:
    pass


FESTIVITY_ROOT_FOLDER_FILE_PATH = 'FESTIVITY_ROOT_FOLDER_FILE_PATH'
CHARACTER_MODEL_FOLDER_FILE_PATH = 'CHARACTER_MODEL_FOLDER_FILE_PATH'
BL_IDNAME_FUNCTION = 'function_to_call'
ENABLED = 'enabled'
CACHE_KEY = 'cache'

cache = {
    FESTIVITY_ROOT_FOLDER_FILE_PATH: '',
    CHARACTER_MODEL_FOLDER_FILE_PATH: ''
}

steps = {
    1: {
        BL_IDNAME_FUNCTION: bpy.ops.file.genshin_import_materials,
        ENABLED: True,
        CACHE_KEY: ''
    },
    2: {
        BL_IDNAME_FUNCTION: join_body_parts_to_body,
        ENABLED: False,
        CACHE_KEY: ''
    },
    3: {
        BL_IDNAME_FUNCTION: bpy.ops.file.genshin_import_model,
        ENABLED: True,
        CACHE_KEY: ''
    },
    4: {
        BL_IDNAME_FUNCTION: bpy.ops.file.genshin_import_textures,
        ENABLED: True,
        CACHE_KEY: CHARACTER_MODEL_FOLDER_FILE_PATH
    },
    5: {
        BL_IDNAME_FUNCTION: bpy.ops.file.genshin_import_material_data,
        ENABLED: True,
        CACHE_KEY: ''
    }
}


def invoke_next_step(current_step_idx: int, file_path_to_cache=None):
    if current_step_idx <= 0 or current_step_idx > len(steps):
        return
    # Disabled cache, it does not work as intended b/c it carries over from past usage
    # if file_path_to_cache is not None and steps[current_step_idx][CACHE_KEY]:
    #     cache_file_path(current_step_idx - 1, file_path_to_cache)
    
    if steps[current_step_idx][ENABLED]:
        cached_file_directory = cache.get(steps[current_step_idx][CACHE_KEY], '')
        execute_or_invoke = 'EXEC' if cached_file_directory else 'INVOKE'
        function_to_use = steps[current_step_idx][BL_IDNAME_FUNCTION]

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


def cache_file_path(last_step_idx, file_path_to_cache):
    # if steps[last_step_idx][BL_IDNAME_FUNCTION] == steps[1][BL_IDNAME_FUNCTION]:
    #     cache[FESTIVITY_ROOT_FOLDER_FILE_PATH] = file_path_to_cache
    # elif steps[last_step_idx][BL_IDNAME_FUNCTION] == steps[2][BL_IDNAME_FUNCTION] or steps[last_step_idx] == steps[3][BL_IDNAME_FUNCTION]:
    #     cache[CHARACTER_MODEL_FOLDER_FILE_PATH] = file_path_to_cache
    
    step = steps[last_step_idx]
    step_cache_key = step.get(CACHE_KEY)

    print(f'Assigning `{step_cache_key}:{file_path_to_cache}` in cache')
    cache[step_cache_key] = file_path_to_cache
