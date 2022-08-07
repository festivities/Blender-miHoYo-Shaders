# Written by Mken from Discord

import bpy

try:
    import scripts.setup_wizard.import_order
except:
    print("ERROR: Couldn't import invoke_next_step, but it's not needed if running this as a standalone")

do_not_delete_object_list = [
    'Camera',
    'Face Light Direction',
    'Head Driver',
    'Hemi',
    'Light',
    'Main Light Direction'
]


def delete_empties(next_step_idx):
    scene = bpy.context.scene

    for object in scene.objects:
        if object.type == 'EMPTY' and object.name not in do_not_delete_object_list:
            bpy.data.objects.remove(object)

    if next_step_idx:
        scripts.setup_wizard.import_order.invoke_next_step(next_step_idx)


if __name__ == '__main__':
    delete_empties(None)
