# Written by Mken from Discord

import bpy

try:
    import scripts.setup_wizard.import_order
except:
    print("ERROR: Couldn't import invoke_next_step, but it's not needed if running this as a standalone")

HEAD_DRIVER_OBJECT_NAME = 'Head Driver'


def setup_head_driver(next_step_index):
    head_driver_object = bpy.data.objects.get(HEAD_DRIVER_OBJECT_NAME)
    child_of_constraint = head_driver_object.constraints[0]  # expecting 1 constraint head driver

    armature = [object for object in bpy.data.objects if object.type == 'ARMATURE'][0]  # expecting 1 armature
    armature_bones = armature.data.bones
    head_bone_name = [bone_name for bone_name in armature_bones.keys() if 'Head' in bone_name][0]  # expecting 1 bone with Head in the name

    set_contraint_target_and_bone(child_of_constraint, armature, head_bone_name)
    set_inverse(head_driver_object)

    if next_step_index:
        scripts.setup_wizard.import_order.invoke_next_step(next_step_index)


def set_contraint_target_and_bone(constraint, armature, bone_name):
    constraint.target = armature
    constraint.subtarget = bone_name


def set_inverse(object):
    bpy.context.view_layer.objects.active = object
    bpy.ops.constraint.childof_set_inverse(constraint="Child Of", owner='OBJECT')


if __name__ == '__main__':
    setup_head_driver(None)
