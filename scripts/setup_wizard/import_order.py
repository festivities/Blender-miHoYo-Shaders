# Written by Mken from Discord
# Kudos to Modder4869 for introducing another way to get the real material name for Dress materials

import bpy
import json

try:
    # Really ugly in my opinion, but this let's us reload modules when we make changes to them without
    # having to restart Blender (not quite sure if this works yet in this module!!)
    import importlib
    import scripts.setup_wizard.join_body_parts_to_body
    import scripts.setup_wizard.genshin_setup_geometry_nodes
    import scripts.setup_wizard.fix_mouth_outlines
    import scripts.setup_wizard.delete_empties
    import scripts.setup_wizard.delete_specific_objects
    import scripts.setup_wizard.misc_final_steps
    import scripts.setup_wizard.setup_head_driver

    importlib.reload(scripts.setup_wizard.join_body_parts_to_body)
    importlib.reload(scripts.setup_wizard.genshin_setup_geometry_nodes)
    importlib.reload(scripts.setup_wizard.fix_mouth_outlines)
    importlib.reload(scripts.setup_wizard.delete_empties)
    importlib.reload(scripts.setup_wizard.delete_specific_objects)
    importlib.reload(scripts.setup_wizard.misc_final_steps)
    importlib.reload(scripts.setup_wizard.setup_head_driver)
except:
    print('Exception when trying to import required dependency scripts!')

# Config Constants
COMPONENT_NAME = 'component_name'
ENABLED = 'enabled'
CACHE_KEY = 'cache_key'

# Cache Constants
FESTIVITY_ROOT_FOLDER_FILE_PATH = 'festivity_root_folder_file_path'
CHARACTER_MODEL_FOLDER_FILE_PATH = 'character_model_folder_file_path'

path_to_setup_wizard_folder = ''

def invoke_next_step(current_step_idx: int, file_path_to_cache=None, path_to_streamlined_setup=''):
    if path_to_streamlined_setup:
        global path_to_setup_wizard_folder
        path_to_setup_wizard_folder = path_to_streamlined_setup

    # We use a config.json so that we can make changes without having to restart Blender
    # TODO: Make this a class that gets instantiated in each component? 
    # TOOD: Making a class may allow us to move config.json data back into this module?
    file = open(f'{path_to_setup_wizard_folder}/config.json')
    config = json.load(file)

    cache_file_path = f'{path_to_setup_wizard_folder}/cache.json.tmp'
    if current_step_idx == 1:
        with open(cache_file_path, 'w') as f:
            json.dump({}, f)
    cache_file = open(cache_file_path)
    cache = json.load(cache_file)


    if current_step_idx <= 0 or current_step_idx + 1 > len(config):  # +1 because we have a step 0
        return

    previous_step = config.get(str(current_step_idx - 1))
    if file_path_to_cache and previous_step and previous_step[CACHE_KEY]:
        cache_previous_step_file_path(cache, previous_step, file_path_to_cache)
        with open(cache_file_path, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=4)
    
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


def cache_previous_step_file_path(cache, last_step, file_path_to_cache):
    step_cache_key = last_step.get(CACHE_KEY)

    print(f'Assigning `{step_cache_key}:{file_path_to_cache}` in cache')
    cache[step_cache_key] = file_path_to_cache


def get_actual_material_name_for_dress(material_name):
    for material in bpy.data.materials:
        if material_name in material.name:
            # ex. 'Avatar_Lady_Pole_Rosaria_Tex_Body_Diffuse.png'
            base_color_texture_image_name = material.node_tree.nodes['Principled BSDF'].inputs['Base Color'].links[0].from_node.image.name_full
            actual_material_name = base_color_texture_image_name.split('_')[-2]
            actual_material_name = actual_material_name if actual_material_name else 'Hair' \
                if 'Hair' in base_color_texture_image_name else 'Body'  # fallback method to get mat name
            return actual_material_name


class ComponentFunctionFactory:
    @staticmethod
    def create_component_function(component_name):
        if component_name == 'import_materials':
            return bpy.ops.file.genshin_import_materials
        elif component_name == 'join_body_parts_to_body':
            return scripts.setup_wizard.join_body_parts_to_body.join_body_parts_to_body
        elif component_name == 'import_character_model':
            return bpy.ops.file.genshin_import_model
        elif component_name == 'replace_default_materials':
            return bpy.ops.file.genshin_replace_default_materials
        elif component_name == 'import_character_textures':
            return bpy.ops.file.genshin_import_textures
        elif component_name == 'import_outlines':
            return bpy.ops.file.genshin_import_outlines
        elif component_name == 'setup_geometry_nodes':
            return scripts.setup_wizard.genshin_setup_geometry_nodes.setup_geometry_nodes
        elif component_name == 'import_outline_lightmaps':
            return bpy.ops.file.genshin_import_outline_lightmaps
        elif component_name == 'import_material_data':
            return bpy.ops.file.genshin_import_material_data
        elif component_name == 'fix_mouth_outlines':
            return scripts.setup_wizard.fix_mouth_outlines.fix_face_mouth_outlines_protruding_out
        elif component_name == 'delete_empties':
            return scripts.setup_wizard.delete_empties.delete_empties
        elif component_name ==  'delete_specific_objects':
            return scripts.setup_wizard.delete_specific_objects.delete_specified_objects
        elif component_name == 'make_character_upright':
            return scripts.setup_wizard.misc_final_steps.make_character_upright
        elif component_name == 'set_color_management_to_standard':
            return scripts.setup_wizard.misc_final_steps.set_color_management_to_standard
        elif component_name == 'setup_head_driver':
            return scripts.setup_wizard.setup_head_driver.setup_head_driver
        else:
            raise Exception(f'Unknown component name passed into {__name__}: {component_name}')