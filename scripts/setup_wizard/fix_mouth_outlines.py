# Written by Mken from Discord

import bpy

try:
    import scripts.setup_wizard.import_order
except:
    print("ERROR: Couldn't import invoke_next_step, but it's not needed if running this as a standalone")

CAMERA_INPUT = 'Input_4'
DEPTH_OFFSET_INPUT = 'Input_8'

CAMERA_NAME = 'Camera'
FACE_MESH_NAME = 'Face'
FACE_EYE_MESH_NAME = 'Face_Eye'
GEOMETRY_NODES_PREFIX = 'GeometryNodes'


def fix_face_mouth_outlines_protruding_out(next_step_idx):
    camera = bpy.context.scene.objects.get(CAMERA_NAME)
    if not camera:
        camera = create_camera(CAMERA_NAME)

    face_objects = [object for object in bpy.data.objects \
        if FACE_MESH_NAME in object.name and FACE_EYE_MESH_NAME not in object.name]
    for face_object in face_objects:
        outline_modifiers = [outline_modifier for outline_modifier in face_object.modifiers.values() \
            if GEOMETRY_NODES_PREFIX in outline_modifier.name]
        set_camera_and_depth_offset(outline_modifiers, camera)
        fix_meshes_by_setting_genshin_materials(face_object.name)

    if next_step_idx:
        scripts.setup_wizard.import_order.invoke_next_step(next_step_idx)


def set_camera_and_depth_offset(outline_modifiers, camera):
    for outline_modifier in outline_modifiers:
        outline_modifier[CAMERA_INPUT] = camera
        outline_modifier[DEPTH_OFFSET_INPUT] = 3.0
        set_camera_in_front_of_armature(camera)


def create_camera(camera_name):
    camera_data = bpy.data.cameras.new(name=camera_name)
    camera = bpy.data.objects.new(camera_name, camera_data)
    bpy.context.scene.collection.objects.link(camera)

    return camera


def set_camera_in_front_of_armature(camera):
    for object in bpy.context.scene.objects:
        if object.type == 'ARMATURE':
            camera.location = object.location
            break
    camera.location[1] += -1.5  # y-axis, facing character
    camera.location[2] += 1.3  # z-axis, head level
    camera.rotation_euler[0] = 1.5708  # x-axis, 90 degrees 
    camera.rotation_euler[2] = 0  # z-axis, facing character


def fix_meshes_by_setting_genshin_materials(mesh_name):
    for material_slot_name, material_slot in bpy.context.scene.objects[mesh_name].material_slots.items():
        bpy.context.scene.objects[mesh_name].material_slots.get(material_slot_name).material = material_slot.material


def main():
    fix_face_mouth_outlines_protruding_out(None)


if __name__ == '__main__':
    main()
