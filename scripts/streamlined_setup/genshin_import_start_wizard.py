# Written by Mken from Discord

import bpy
from bpy.types import Operator

import sys
if './scripts/streamlined_setup' not in sys.path:
    sys.path.append('./scripts/streamlined_setup')

from import_order import invoke_next_step
from genshin_import_materials import GI_OT_GenshinImportMaterials
from genshin_import_character_model import GI_OT_GenshinImportModel
from genshin_import_textures import GI_OT_GenshinImportTextures


class GI_OT_GenshinImportWizard(Operator):
    """Import Wizard Process"""
    bl_idname = "file.genshin_import_wizard"
    bl_label = "Genshin: Import Wizard (Start Here!)"

    def execute(self, context):
        invoke_next_step(1)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(GI_OT_GenshinImportWizard)

    # Originally I tried checking, but this way is less bug-prone and is more Pythonic
    # Tried checking for attributes (on bpy.ops.file.xxx), but it seemed to always return true
    for class_to_register in [GI_OT_GenshinImportMaterials, GI_OT_GenshinImportModel, GI_OT_GenshinImportTextures]:
        try:
            bpy.utils.register_class(class_to_register)
        except ValueError:
            pass  # expected if class is already registered


def unregister():
    bpy.utils.unregister_class(GI_OT_GenshinImportMaterials)
    bpy.utils.unregister_class(GI_OT_GenshinImportModel)
    bpy.utils.unregister_class(GI_OT_GenshinImportTextures)


if __name__ == "__main__":
    register()
