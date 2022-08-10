# Structure for class comes from a script initially written by Zekium from Discord
# Written by Mken from Discord

import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator

import os


class GI_OT_GenshinSetupWizard(Operator, ImportHelper):
    """Setup Wizard Process"""
    bl_idname = "file.genshin_setup_wizard"
    bl_label = "Genshin: Setup Wizard - Select Festivity's Shaders Folder"

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
        invoke_next_step = setup_dependencies(self.filepath)
        invoke_next_step(
            1, 
            file_path_to_cache = self.filepath, 
            path_to_streamlined_setup=os.path.join(self.filepath, 'scripts/' 'setup_wizard/')
        )

        return {'FINISHED'}


def register():
    bpy.utils.register_class(GI_OT_GenshinSetupWizard)


# Specifically done this way because path is dependent on where Blender is started
# We ask for the filepath to Festivity's shaders that way we can set up the scripts in the path
def setup_dependencies(filepath):
    directory = os.path.dirname(filepath)

    import sys
    if filepath not in sys.path:
        sys.path.append(directory)

    # Really ugly in my opinion, but this let's us reload modules when we make changes to them without
    # having to restart Blender.
    import importlib
    import scripts.setup_wizard.import_order
    import scripts.setup_wizard.genshin_import_character_model
    import scripts.setup_wizard.genshin_import_material_data
    import scripts.setup_wizard.genshin_import_materials
    import scripts.setup_wizard.genshin_import_outline_lightmaps
    import scripts.setup_wizard.genshin_import_outlines
    import scripts.setup_wizard.genshin_import_textures
    import scripts.setup_wizard.genshin_replace_default_materials

    importlib.reload(scripts.setup_wizard.import_order)
    importlib.reload(scripts.setup_wizard.genshin_import_character_model)
    importlib.reload(scripts.setup_wizard.genshin_import_material_data)
    importlib.reload(scripts.setup_wizard.genshin_import_materials)
    importlib.reload(scripts.setup_wizard.genshin_import_outline_lightmaps)
    importlib.reload(scripts.setup_wizard.genshin_import_outlines)
    importlib.reload(scripts.setup_wizard.genshin_import_textures)
    importlib.reload(scripts.setup_wizard.genshin_replace_default_materials)

    for class_to_register in [
        scripts.setup_wizard.genshin_import_character_model.GI_OT_GenshinImportModel,
        scripts.setup_wizard.genshin_import_material_data.GI_OT_GenshinImportMaterialData,
        scripts.setup_wizard.genshin_import_materials.GI_OT_GenshinImportMaterials,
        scripts.setup_wizard.genshin_import_outline_lightmaps.GI_OT_GenshinImportOutlineLightmaps,
        scripts.setup_wizard.genshin_import_outlines.GI_OT_GenshinImportOutlines,
        scripts.setup_wizard.genshin_import_textures.GI_OT_GenshinImportTextures,
        scripts.setup_wizard.genshin_replace_default_materials.GI_OT_GenshinReplaceDefaultMaterials,
        ]:
        try:
            bpy.utils.register_class(class_to_register)
        except ValueError:
            pass  # expected if class is already registered
    return scripts.setup_wizard.import_order.invoke_next_step


# Need to have run setup_dependencies in order to unregister, otherwise sys.path 
# will be missing the filepath to the scripts folder
def unregister():
    from scripts.setup_wizard.genshin_import_materials import GI_OT_GenshinImportMaterials
    from scripts.setup_wizard.genshin_import_character_model import GI_OT_GenshinImportModel
    from scripts.setup_wizard.genshin_replace_default_materials import GI_OT_GenshinReplaceDefaultMaterials
    from scripts.setup_wizard.genshin_import_textures import GI_OT_GenshinImportTextures
    from scripts.setup_wizard.genshin_import_outlines import GI_OT_GenshinImportOutlines
    from scripts.setup_wizard.genshin_import_outline_lightmaps import GI_OT_GenshinImportOutlineLightmaps
    from scripts.setup_wizard.genshin_import_material_data import GI_OT_GenshinImportMaterialData

    bpy.utils.unregister_class(GI_OT_GenshinImportMaterials)
    bpy.utils.unregister_class(GI_OT_GenshinImportModel)
    bpy.utils.unregister_class(GI_OT_GenshinReplaceDefaultMaterials)
    bpy.utils.unregister_class(GI_OT_GenshinImportTextures)
    bpy.utils.unregister_class(GI_OT_GenshinImportOutlines)
    bpy.utils.unregister_class(GI_OT_GenshinImportOutlineLightmaps)
    bpy.utils.unregister_class(GI_OT_GenshinImportMaterialData)


if __name__ == "__main__":
    register()
