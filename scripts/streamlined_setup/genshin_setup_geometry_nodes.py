# Written by Mken from Discord

import bpy

# Notes:
# Create GeometryNodes for each Mesh under the Armature
# Assign to the Mask the Materials that are under that Mesh
# EyeStar, Brow, probably don't need Outlines, but..oh well, that's probably fine


# Constants
NAME_OF_GEOMETRY_NODES_MODIFIER = 'GeometryNodes'
NAME_OF_VERTEX_COLORS_INPUT = 'Input_3'
NAME_OF_OUTLINE_THICKNESS_INPUT = 'Input_7'
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


def main():
    for mesh in meshes_to_create_geometry_nodes_on:
        create_geometry_nodes_modifier(f'{mesh}{BODY_PART_SUFFIX}')
    fix_meshes_by_setting_any_genshin_material()
    # configure_genshin_outlines_color()


def create_geometry_nodes_modifier(mesh_name):
    mesh = bpy.context.scene.objects[mesh_name]
    outlines_node_group = bpy.data.node_groups.get('miHoYo - Outlines')

    geometry_nodes_modifier = mesh.modifiers.get(f'{NAME_OF_GEOMETRY_NODES_MODIFIER} {mesh_name}')

    if not geometry_nodes_modifier:
        geometry_nodes_modifier = mesh.modifiers.new(f'{NAME_OF_GEOMETRY_NODES_MODIFIER} {mesh_name}', 'NODES')
        geometry_nodes_modifier.node_group = outlines_node_group

    setup_modifier_default_values(geometry_nodes_modifier, mesh)
    return geometry_nodes_modifier


def setup_modifier_default_values(modifier, mesh):
    # if bpy.context.object.modifiers[f'{NAME_OF_GEOMETRY_NODES_MODIFIER}{mesh.name}'][f'{NAME_OF_VERTEX_COLORS_INPUT}_use_attribute'] == 0:
    if modifier[f'{NAME_OF_VERTEX_COLORS_INPUT}_use_attribute'] == 0:
        # Important! Override object key so we don't use the context (ex. selected object)
        bpy.ops.object.geometry_nodes_input_attribute_toggle(
            {"object": bpy.data.objects[mesh.name]},
            prop_path=f"[\"{NAME_OF_VERTEX_COLORS_INPUT}_use_attribute\"]", 
            modifier_name=modifier.name)

    modifier[f'{NAME_OF_VERTEX_COLORS_INPUT}_attribute_name'] = 'Col'

    for (mask_input, material_input), material in zip(outline_mask_to_material_mapping.items(), mesh.material_slots):
        modifier[mask_input] = bpy.data.materials[material.name]
        modifier[material_input] = bpy.data.materials['miHoYo - Genshin Outlines']


def fix_meshes_by_setting_any_genshin_material():
    body_mesh = bpy.context.scene.objects['Body']
    body_mesh.material_slots.get('miHoYo - Genshin Body').material = bpy.data.materials.get('miHoYo - Genshin Body')


# def configure_genshin_outlines_color():
#     bpy.data.materials["miHoYo - Genshin Outlines"]
#     bpy.data.materials["miHoYo - Genshin Outlines"].node_tree.nodes.active.inputs[1].default_value = (0.073, 0.027, 0.008, 1)


if __name__ == '__main__':
    main()
