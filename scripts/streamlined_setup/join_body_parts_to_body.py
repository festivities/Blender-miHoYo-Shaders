import bpy

try:
    import import_order
except:
    print("ERROR: Couldn't import invoke_next_step, run the first step in setup_wizard")


def join_body_parts_to_body(next_step_idx):
    character_model = None
    for object in bpy.context.scene.objects:
        if object.type == 'ARMATURE':
            character_model = object
            continue

    character_model_body = [body_part for body_part in character_model.children if body_part.name == 'Body'][0]
    character_model_children = [body_part for body_part in character_model.children if body_part]
    
    for character_model_child in character_model_children:
        print(f'Selecting {character_model_child} to join')
        character_model_child.select_set(True)
    bpy.context.view_layer.objects.active = character_model_body
    print(f'Joining children body parts to {character_model_body}')
    bpy.ops.object.join()

    import_order.invoke_next_step(next_step_idx)


if __name__ == '__main__':
    # If you run this script as a standalone, it will not run other steps (-1 value set below)
    join_body_parts_to_body(-1)
