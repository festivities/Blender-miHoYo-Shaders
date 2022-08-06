# Written by Mken from Discord

import bpy

try:
    import scripts.setup_wizard.import_order
except:
    print("ERROR: Couldn't import invoke_next_step, but it's not needed if running this as a standalone")

# Constants
NAME_OF_GEOMETRY_NODES_MODIFIER = 'GeometryNodes'
NAME_OF_VERTEX_COLORS_INPUT = 'Input_3'
OUTLINE_THICKNESS_INPUT = 'Input_7'
BODY_PART_SUFFIX = ''

NAME_OF_OUTLINE_1_MASK_INPUT = 'Input_10'
NAME_OF_OUTLINE_1_MATERIAL_INPUT = 'Input_5'
NAME_OF_OUTLINE_2_MASK_INPUT = 'Input_11'
NAME_OF_OUTLINE_2_MATERIAL_INPUT = 'Input_9'
NAME_OF_OUTLINE_3_MASK_INPUT = 'Input_14'
NAME_OF_OUTLINE_3_MATERIAL_INPUT = 'Input_15'
NAME_OF_OUTLINE_4_MASK_INPUT = 'Input_18'
NAME_OF_OUTLINE_4_MATERIAL_INPUT = 'Input_19'


outline_mask_to_material_mapping = {
    NAME_OF_OUTLINE_1_MASK_INPUT: NAME_OF_OUTLINE_1_MATERIAL_INPUT,
    NAME_OF_OUTLINE_2_MASK_INPUT: NAME_OF_OUTLINE_2_MATERIAL_INPUT,
    NAME_OF_OUTLINE_3_MASK_INPUT: NAME_OF_OUTLINE_3_MATERIAL_INPUT,
    NAME_OF_OUTLINE_4_MASK_INPUT: NAME_OF_OUTLINE_4_MATERIAL_INPUT
}

meshes_to_create_geometry_nodes_on = [
    'Body',
    'Brow',
    'Face',
    'Face_Eye'
]

face_meshes = [
    'Brow',
    'Face',
    'Face_Eye'
]


def setup_geometry_nodes(next_step_idx):
    clone_outlines()
    for mesh_name in meshes_to_create_geometry_nodes_on:
        create_geometry_nodes_modifier(f'{mesh_name}{BODY_PART_SUFFIX}')
        fix_meshes_by_setting_genshin_materials(mesh_name)

    if next_step_idx:
        scripts.setup_wizard.import_order.invoke_next_step(next_step_idx)


def create_geometry_nodes_modifier(mesh_name):
    mesh = bpy.context.scene.objects[mesh_name]
    outlines_node_group = bpy.data.node_groups.get('miHoYo - Outlines')

    geometry_nodes_modifier = mesh.modifiers.get(f'{NAME_OF_GEOMETRY_NODES_MODIFIER} {mesh_name}')

    if not geometry_nodes_modifier:
        geometry_nodes_modifier = mesh.modifiers.new(f'{NAME_OF_GEOMETRY_NODES_MODIFIER} {mesh_name}', 'NODES')
        geometry_nodes_modifier.node_group = outlines_node_group

    setup_modifier_default_values(geometry_nodes_modifier, mesh)
    return geometry_nodes_modifier


def clone_outlines():
    materials = bpy.data.materials.values()

    for material in materials:
        if 'miHoYo - Genshin' in material.name and material.name != 'miHoYo - Genshin Outlines':
            outline_material = bpy.data.materials.get('miHoYo - Genshin Outlines')
            new_outline_name = f'{material.name} Outlines'

            new_outline_material = outline_material.copy()
            new_outline_material.name = new_outline_name


def setup_modifier_default_values(modifier, mesh):
    if modifier[f'{NAME_OF_VERTEX_COLORS_INPUT}_use_attribute'] == 0:
        # Important! Override object key so we don't use the context (ex. selected object)
        bpy.ops.object.geometry_nodes_input_attribute_toggle(
            {"object": bpy.data.objects[mesh.name]},
            prop_path=f"[\"{NAME_OF_VERTEX_COLORS_INPUT}_use_attribute\"]", 
            modifier_name=modifier.name)

    modifier[f'{NAME_OF_VERTEX_COLORS_INPUT}_attribute_name'] = 'Col'

    if mesh.name == 'Face_Eye':
        disable_face_eye_outlines(modifier)

    for (mask_input, material_input), material in zip(outline_mask_to_material_mapping.items(), mesh.material_slots):
        modifier[mask_input] = bpy.data.materials[material.name]
        modifier[material_input] = bpy.data.materials[f'{material.name} Outlines']


def disable_face_eye_outlines(modifier):
    # Specifically do not try to get modifiers from context because context does not have newly
    # created geometry nodes yet during the setup_wizard!! (or it just doesn't work in general)
    # face_eye_outlines = bpy.context.object.modifiers.get('GeometryNodes Face_Eye')  # Bad!
    modifier[OUTLINE_THICKNESS_INPUT] = 0.0


def fix_meshes_by_setting_genshin_materials(mesh_name):
    for material_slot_name, material_slot in bpy.context.scene.objects[mesh_name].material_slots.items():
        bpy.context.scene.objects[mesh_name].material_slots.get(material_slot_name).material = material_slot.material


if __name__ == '__main__':
    setup_geometry_nodes(None)
