# Written by Mken from Discord

import bpy

try:
    import scripts.setup_wizard.import_order
except:
    print("ERROR: Couldn't import invoke_next_step, but it's not needed if running this as a standalone")

objects_to_delete = [
    'EffectMesh'
]


def delete_specified_objects(next_step_idx):
    scene = bpy.context.scene

    for object in scene.objects:
        if object.name in objects_to_delete:
            bpy.data.objects.remove(object)

    if next_step_idx:
        scripts.setup_wizard.import_order.invoke_next_step(next_step_idx)


if __name__ == '__main__':
    delete_specified_objects(None)
