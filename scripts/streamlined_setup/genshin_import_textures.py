# Contributed by Zekium and Modder4869 from Discord - huge thanks to him!

import bpy

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, IntProperty, BoolProperty, EnumProperty
from bpy.types import Operator
import os

# TOOD: Fix imports (requires you to at least do the first step in Import Wizard!)
import sys
if './scripts/streamlined_setup' not in sys.path:
    sys.path.append('./scripts/streamlined_setup')

from import_order import invoke_next_step


class GI_OT_GenshinImportTextures(Operator, ImportHelper):
    """Select the folder with the model's textures to import"""
    bl_idname = "file.genshin_import_textures"  # important since its how we chain file dialogs
    bl_label = "3_Genshin: Select Texture Folder"

    # ImportHelper mixin class uses this
    filename_ext = "*.*"
    
    import_path: StringProperty(
        name = "Path",
        description = "Path to the folder containing the files to import",
        default = "",
        subtype = 'DIR_PATH'
        )

    filter_glob: StringProperty(
        default="*.*",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    next_step_idx: IntProperty()
    file_directory: StringProperty()

    material_assignment_mapping = {
        'Yelan': {
            'miHoYo - Genshin Dress1': 'Body',
            'miHoYo - Genshin Dress2': 'Hair'
        },
        'Collei': {
            'miHoYo - Genshin Dress': 'Hair'
        },
        'Ganyu': {
            'miHoYo - Genshin Dress': 'Body'
        },
        'Rosaria': {
            'miHoYo - Genshin Dress1': 'Hair',
            'miHoYo - GEnshin Dress2': 'Body'
        }
    }

    def execute(self, context):
        directory = self.file_directory if self.file_directory else os.path.dirname(self.filepath)

        print(self.file_directory)
        print(self.filepath)
        
        for name, folder, files in os.walk(directory):
            character_name = ''
            for file in files:
                for tmp_character_name in self.material_assignment_mapping.keys():
                    if tmp_character_name in file:
                        character_name = tmp_character_name

            for file in files :
                # load the file with the correct alpha mode
                img_path = directory + "/" + file
                img = bpy.data.images.load(filepath = img_path, check_existing=True)
                img.alpha_mode = 'CHANNEL_PACKED'
                
                # declare body and face mesh variables
                body_mesh = bpy.context.scene.objects.get("Body")
                face_mesh = bpy.context.scene.objects.get("Face")

                print(file)
                
                # Implement the texture in the correct node
                if "Hair_Diffuse" in file :
                    bpy.context.view_layer.objects.active = body_mesh
                    bpy.context.object.material_slots.get('miHoYo - Genshin Hair').material.node_tree.nodes['Hair_Diffuse_UV0'].image = img
                    bpy.context.object.material_slots.get('miHoYo - Genshin Hair').material.node_tree.nodes['Hair_Diffuse_UV1'].image = img
                    self.setup_dress_textures(character_name, 'Hair_Diffuse', img)
                elif "Hair_Lightmap" in file :
                    bpy.context.view_layer.objects.active = body_mesh
                    img.colorspace_settings.name='Non-Color'
                    bpy.context.object.material_slots.get('miHoYo - Genshin Hair').material.node_tree.nodes['Hair_Lightmap_UV0'].image = img
                    bpy.context.object.material_slots.get('miHoYo - Genshin Hair').material.node_tree.nodes['Hair_Lightmap_UV1'].image = img
                    self.setup_dress_textures(character_name, 'Hair_Lightmap', img)
                elif "Hair_Normalmap" in file :
                    bpy.context.view_layer.objects.active = body_mesh
                    img.colorspace_settings.name='Non-Color'
                    bpy.context.object.material_slots.get('miHoYo - Genshin Hair').material.node_tree.nodes['Hair_Normalmap_UV0'].image = img
                    bpy.context.object.material_slots.get('miHoYo - Genshin Hair').material.node_tree.nodes['Hair_Normalmap_UV1'].image = img
                    self.setup_dress_textures(character_name, 'Hair_Normalmap', img)
                elif "Hair_Shadow_Ramp" in file :
                    bpy.data.node_groups['Hair Shadow Ramp'].nodes['Hair_Shadow_Ramp'].image = img
                elif "Body_Diffuse" in file :
                    bpy.context.view_layer.objects.active = body_mesh
                    bpy.context.object.material_slots.get('miHoYo - Genshin Body').material.node_tree.nodes['Body_Diffuse_UV0'].image = img
                    bpy.context.object.material_slots.get('miHoYo - Genshin Body').material.node_tree.nodes['Body_Diffuse_UV1'].image = img
                    self.setup_dress_textures(character_name, 'Body_Diffuse', img)
                elif "Body_Lightmap" in file :
                    bpy.context.view_layer.objects.active = body_mesh
                    img.colorspace_settings.name='Non-Color'
                    bpy.context.object.material_slots.get('miHoYo - Genshin Body').material.node_tree.nodes['Body_Lightmap_UV0'].image = img
                    bpy.context.object.material_slots.get('miHoYo - Genshin Body').material.node_tree.nodes['Body_Lightmap_UV1'].image = img
                    self.setup_dress_textures(character_name, 'Body_Lightmap', img)
                elif "Body_Normalmap" in file :
                    bpy.context.view_layer.objects.active = body_mesh
                    img.colorspace_settings.name='Non-Color'
                    bpy.context.object.material_slots.get('miHoYo - Genshin Body').material.node_tree.nodes['Body_Normalmap_UV0'].image = img
                    bpy.context.object.material_slots.get('miHoYo - Genshin Body').material.node_tree.nodes['Body_Normalmap_UV1'].image = img
                    self.setup_dress_textures(character_name, 'Body_Normalmap', img)
                elif "Body_Shadow_Ramp" in file :
                    bpy.data.node_groups['Body Shadow Ramp'].nodes['Body_Shadow_Ramp'].image = img
                elif "Face_Diffuse" in file :
                    bpy.context.view_layer.objects.active = face_mesh if face_mesh else body_mesh
                    bpy.context.object.material_slots.get('miHoYo - Genshin Face').material.node_tree.nodes['Face_Diffuse'].image = img
                elif "Face_Shadow" in file :
                    bpy.context.view_layer.objects.active = face_mesh if face_mesh else body_mesh
                    img.colorspace_settings.name='Non-Color'
                    bpy.context.object.material_slots.get('miHoYo - Genshin Face').material.node_tree.nodes['Face_Shadow'].image = img
                elif "FaceLightmap" in file :
                    bpy.context.view_layer.objects.active = face_mesh if face_mesh else body_mesh
                    img.colorspace_settings.name='Non-Color'
                    bpy.data.node_groups['Face Lightmap'].nodes['Face_Lightmap'].image = img
                elif "MetalMap" in file :
                    bpy.data.node_groups['Metallic Matcap'].nodes['MetalMap'].image = img
                else :
                    pass

        print('Imported textures...')
        invoke_next_step(self.next_step_idx, directory)
        return {'FINISHED'}
    
    def setup_dress_textures(self, character_name, texture_name, texture_img):
        material_mapping = self.material_assignment_mapping.get(character_name)

        if material_mapping:
            for material_name, body_part in material_mapping.items():
                if body_part in texture_name:
                    material_shader_nodes = bpy.data.materials.get(material_name).node_tree.nodes
                    material_shader_nodes.get(f'{texture_name}_UV0').image = texture_img
                    material_shader_nodes.get(f'{texture_name}_UV1').image = texture_img

        # If not found it mapping, default Dress to Body (if current texture_name has Body in it)
        if 'Body' in texture_name:
            dress = bpy.data.materials.get('miHoYo - Genshin Dress')
            if dress:
                dress_shader_nodes = dress.node_tree.nodes
                dress_shader_nodes.get(f'{texture_name}_UV0').image = texture_img
                dress_shader_nodes.get(f'{texture_name}_UV1').image = texture_img
        return




def register():
    bpy.utils.register_class(GI_OT_GenshinImportTextures)


def unregister():
    bpy.utils.unregister_class(GI_OT_GenshinImportTextures)


if __name__ == "__main__":
    register()