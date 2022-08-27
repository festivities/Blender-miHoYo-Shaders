# Contributed by Zekium and Modder4869 from Discord - huge thanks to him!
# Minor changes by Mken

import bpy

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, IntProperty, BoolProperty, EnumProperty
from bpy.types import Operator
import os

try:
    from scripts.setup_wizard.import_order import invoke_next_step
    from scripts.setup_wizard.import_order import get_actual_material_name_for_dress
except Exception:
    print('Error! Run the first step of setup_wizard! Need to set up python script paths')


class GI_OT_GenshinImportTextures(Operator, ImportHelper):
    """Select the folder with the model's textures to import"""
    bl_idname = "file.genshin_import_textures"  # important since its how we chain file dialogs
    bl_label = "Genshin: Import Textures - Select Character Model Folder"

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

    def execute(self, context):
        directory = self.file_directory if self.file_directory else os.path.dirname(self.filepath)
        
        for name, folder, files in os.walk(directory):
            for file in files :
                # load the file with the correct alpha mode
                img_path = directory + "/" + file
                img = bpy.data.images.load(filepath = img_path, check_existing=True)
                img.alpha_mode = 'CHANNEL_PACKED'
                
                # declare body and face mesh variables
                body_mesh = bpy.context.scene.objects.get("Body")
                face_mesh = bpy.context.scene.objects.get("Face")
                
                # Implement the texture in the correct node
                self.report({'INFO'}, f'Importing texture {file}')
                if "Hair_Diffuse" in file :
                    bpy.context.view_layer.objects.active = body_mesh
                    bpy.context.object.material_slots.get('miHoYo - Genshin Hair').material.node_tree.nodes['Hair_Diffuse_UV0'].image = img
                    bpy.context.object.material_slots.get('miHoYo - Genshin Hair').material.node_tree.nodes['Hair_Diffuse_UV1'].image = img
                    self.setup_dress_textures('Hair_Diffuse', img)
                elif "Hair_Lightmap" in file :
                    bpy.context.view_layer.objects.active = body_mesh
                    img.colorspace_settings.name='Non-Color'
                    bpy.context.object.material_slots.get('miHoYo - Genshin Hair').material.node_tree.nodes['Hair_Lightmap_UV0'].image = img
                    bpy.context.object.material_slots.get('miHoYo - Genshin Hair').material.node_tree.nodes['Hair_Lightmap_UV1'].image = img
                    self.setup_dress_textures('Hair_Lightmap', img)
                elif "Hair_Normalmap" in file :
                    bpy.context.view_layer.objects.active = body_mesh
                    img.colorspace_settings.name='Non-Color'
                    bpy.context.object.material_slots.get('miHoYo - Genshin Hair').material.node_tree.nodes['Hair_Normalmap_UV0'].image = img
                    bpy.context.object.material_slots.get('miHoYo - Genshin Hair').material.node_tree.nodes['Hair_Normalmap_UV1'].image = img
                    self.setup_dress_textures('Hair_Normalmap', img)
                elif "Hair_Shadow_Ramp" in file :
                    bpy.data.node_groups['Hair Shadow Ramp'].nodes['Hair_Shadow_Ramp'].image = img
                elif "Body_Diffuse" in file :
                    bpy.context.view_layer.objects.active = body_mesh
                    bpy.context.object.material_slots.get('miHoYo - Genshin Body').material.node_tree.nodes['Body_Diffuse_UV0'].image = img
                    bpy.context.object.material_slots.get('miHoYo - Genshin Body').material.node_tree.nodes['Body_Diffuse_UV1'].image = img
                    self.setup_dress_textures('Body_Diffuse', img)
                elif "Body_Lightmap" in file :
                    bpy.context.view_layer.objects.active = body_mesh
                    img.colorspace_settings.name='Non-Color'
                    bpy.context.object.material_slots.get('miHoYo - Genshin Body').material.node_tree.nodes['Body_Lightmap_UV0'].image = img
                    bpy.context.object.material_slots.get('miHoYo - Genshin Body').material.node_tree.nodes['Body_Lightmap_UV1'].image = img
                    self.setup_dress_textures('Body_Lightmap', img)
                elif "Body_Normalmap" in file :
                    bpy.context.view_layer.objects.active = body_mesh
                    img.colorspace_settings.name='Non-Color'
                    bpy.context.object.material_slots.get('miHoYo - Genshin Body').material.node_tree.nodes['Body_Normalmap_UV0'].image = img
                    bpy.context.object.material_slots.get('miHoYo - Genshin Body').material.node_tree.nodes['Body_Normalmap_UV1'].image = img
                    self.setup_dress_textures('Body_Normalmap', img)
                elif "Body_Shadow_Ramp" in file :
                    bpy.data.node_groups['Body Shadow Ramp'].nodes['Body_Shadow_Ramp'].image = img
                elif "Body_Specular_Ramp" in file or "Tex_Specular_Ramp" in file :
                    img.colorspace_settings.name='Non-Color'
                    bpy.data.node_groups['Body Specular Ramp'].nodes['Body_Specular_Ramp'].image = img
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
            break  # IMPORTANT: We os.walk which also traverses through folders...we just want the files

        self.report({'INFO'}, 'Imported textures')
        invoke_next_step(self.next_step_idx, directory)
        return {'FINISHED'}
    
    def setup_dress_textures(self, texture_name, texture_img):
        shader_dress_materials = [material for material in bpy.data.materials if 'Genshin Dress' in material.name]

        for shader_dress_material in shader_dress_materials:
            original_dress_material = [material for material in bpy.data.materials if material.name.endswith(
                shader_dress_material.name.split(' ')[-1]
            )][0]  # the material that ends with 'Dress', 'Dress1', 'Dress2'

            actual_material = get_actual_material_name_for_dress(original_dress_material.name)
            if actual_material in texture_name:
                self.report({'INFO'}, f'Importing texture "{texture_name}" onto material "{shader_dress_material.name}"')
                material_shader_nodes = bpy.data.materials.get(shader_dress_material.name).node_tree.nodes
                material_shader_nodes.get(f'{texture_name}_UV0').image = texture_img
                material_shader_nodes.get(f'{texture_name}_UV1').image = texture_img
                return


def register():
    bpy.utils.register_class(GI_OT_GenshinImportTextures)


def unregister():
    bpy.utils.unregister_class(GI_OT_GenshinImportTextures)


if __name__ == "__main__":
    register()