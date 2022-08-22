# Written by Mken from Discord with support from M4urlcl0!

import bpy

try:
    import scripts.setup_wizard.import_order
except:
    print("ERROR: Couldn't import invoke_next_step, but it's not needed if running this as a standalone")


def make_character_upright(next_step_index):
    bpy.ops.object.select_all(action='DESELECT')
    armature = [object for object in bpy.data.objects if object.type == 'ARMATURE'][0]  # expecting 1 armature
    armature.select_set(True)

    bpy.ops.object.scale_clear()
    bpy.ops.object.rotation_clear()
    armature.rotation_euler[0] = 1.5708  # x-axis, 90 degrees
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)  # needed if you rotate using the above

    # clean rotation
    # bpy.ops.transform.rotate(
    #     value=1.5708, 
    #     orient_axis='X', 
    #     orient_type='GLOBAL', 
    #     orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
    #     orient_matrix_type='GLOBAL', 
    #     constraint_axis=(True, False, False), 
    #     mirror=False, 
    #     use_proportional_edit=False,
    #     proportional_edit_falloff='SMOOTH', 
    #     proportional_size=0.1, 
    #     use_proportional_connected=False, 
    #     use_proportional_projected=False
    # )  # from @M4urlcl0

    if next_step_index:
        scripts.setup_wizard.import_order.invoke_next_step(next_step_index)


def set_color_management_to_standard(next_step_index):
    bpy.context.scene.view_settings.view_transform = 'Standard'

    if next_step_index:
        scripts.setup_wizard.import_order.invoke_next_step(next_step_index)


if __name__ == '__main__':
    make_character_upright(None)
