import bpy

# Contributed by Zekium from Discord - huge thanks to him!!!
# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
import os


class GI_OT_GenshinImportTextures(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "file.genshin_import"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Genshin: Import Textures"

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

    def execute(self, context):
        directory = os.path.dirname(self.filepath)
        
        for name, folder, files in os.walk(directory):
            for file in files :
                # load the file with the correct alpha mode
                img_path = directory + "/" + file
                img = bpy.data.images.load(filepath = img_path, check_existing=True)
                img.alpha_mode = 'CHANNEL_PACKED'
                
                # declare body and face mesh variables
                body_var = bpy.context.scene.objects["Body"]
                face_var = bpy.context.scene.objects["Face"]
                
                # Implement the texture in the correct node
                if "Hair_Diffuse" in file :
                    bpy.context.view_layer.objects.active = body_var
                    bpy.context.object.material_slots[0].material.node_tree.nodes['Hair_Diffuse_UV0'].image = img
                    bpy.context.object.material_slots[0].material.node_tree.nodes['Hair_Diffuse_UV1'].image = img
                elif "Hair_Lightmap" in file :
                    img.colorspace_settings.name='Non-Color'
                    bpy.context.object.material_slots[0].material.node_tree.nodes['Hair_Lightmap_UV0'].image = img
                    bpy.context.object.material_slots[0].material.node_tree.nodes['Hair_Lightmap_UV1'].image = img
                elif "Body_Diffuse" in file :
                    bpy.context.object.material_slots[1].material.node_tree.nodes['Body_Diffuse_UV0'].image = img
                    bpy.context.object.material_slots[1].material.node_tree.nodes['Body_Diffuse_UV1'].image = img
                elif "Body_Lightmap" in file :
                    img.colorspace_settings.name='Non-Color'
                    bpy.context.object.material_slots[1].material.node_tree.nodes['Body_Lightmap_UV0'].image = img
                    bpy.context.object.material_slots[1].material.node_tree.nodes['Body_Lightmap_UV1'].image = img
                elif "Body_Shadow_Ramp" in file :
                    bpy.data.node_groups['Body Shadow Ramp'].nodes['Body_Shadow_Ramp'].image = img
                elif "Hair_Shadow_Ramp" in file :
                    bpy.data.node_groups['Hair Shadow Ramp'].nodes['Hair_Shadow_Ramp'].image = img
                elif "MetalMap" in file :
                    bpy.data.node_groups['Metallic Matcap'].nodes['MetalMap'].image = img
                elif "Face_Diffuse" in file :
                    bpy.context.view_layer.objects.active = face_var
                    bpy.context.object.material_slots[0].material.node_tree.nodes['Face_Diffuse'].image = img
                elif "FaceLightmap" in file :
                    img.colorspace_settings.name='Non-Color'
                    bpy.data.node_groups['Face Lightmap'].nodes['Face_Lightmap'].image = img
            
        return {'FINISHED'}


def register():
    bpy.utils.register_class(GI_OT_GenshinImportTextures)


def unregister():
    bpy.utils.unregister_class(GI_OT_GenshinImportTextures)


if __name__ == "__main__":
    register()