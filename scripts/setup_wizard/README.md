# Blender miHoYo Shaders - Setup Wizard Tool

(You should view this on Github or some other Markdown reader if you aren't!)

The goal of this tool is to streamline the character setup process. Whether it's importing the materials, importing the character model, setting up the outlines (geometry nodes) or configuring the outline colors to be game accurate.

## Important Note
This tool is broken up into many different components. The `config.json` file can be used to enable or disable steps depending on your workflow.

Example:
```
    "2": {
        "component_name": "import_character_model",
        "enabled": true,
        "cache_key": "character_model_folder_file_path",
        "metadata": {
            "description": "Import character model",
            "requires": "Folder with character model fbx file in it"
        }
    },
```

You can disable any step (component) in the Setup Wizard by changing `"enabled": true,` to `"enabled": false,`
* This may be handy in the scenario that you use BetterFBX and do not want to use Blender's vanilla FBX importer.

You can disable the cache for any step by changing `"cache_key": "<whatever value is here>",` to `"cache_key": "",`
* The cache (`cache.json.tmp`) is used to "save" your previous choice for a future step. It gets overwritten each time you run the Setup Wizard and is purely a temporary file.


### Other Notes:
* The `component_name` should NOT be modified. This is how the Setup Wizard triggers the next component.
* Metadata is simply there to help provide human readable information and what each component requires

## Steps (Detailed Guide)

0. Setup Wizard
    * This step starts the Setup Wizard process. It also is **very important** for setting up the Python paths so that the scripts can import dependencies and other scripts.
    * If you are running into an error about `invoke_next_step`, this is likely your issue. You only need to run the very first of the Setup Wizard and then you can close out of the File Explorer window.
    * Select the root folder that contains Festivity's Shaders.
1. Import Materials
    * This step imports `miHoYo - Genshin Hair`, `miHoYo - Genshin Face`, `miHoYo - Genshin Body` and `miHoYo - Genshin Outlines`.
    * Select the root folder that contains Festivity's Shaders.
2. Import Character Model
    * This step imports the character model which should be a .fbx file
    * Select the folder that contains the character model and textures. **It is assumed that the textures for the character are also in this folder.**
3. ~~Join Body Parts to Body~~ **Deprecated. Unsupported.** Just manually Ctrl+J it yourself.
    * Placeholder: Naming Convention of Genshin Materials: `miHoYo - Genshin {Body Part}` where `{Body Part}` is `Hair`, `Body`, `Dress`, `Dress1`, `Dress2`, etc.
    * Yes, this tool also handle special exceptions for characters like: `Yelan`, `Collei` and `Rosaria` who may have their `Dress` set to `Hair` instead of the usual `Body`.
4. Import Character Textures
    * This step imports the character textures and assigns them to the materials imported in Step 1.
    * Yes, this tool also handle special exceptions for characters like: `Yelan`, `Collei` and `Rosaria` who may have their `Dress` set to `Hair` instead of the usual `Body`.
    * **This step uses the cache** so you do not need to select a folder. It uses what was selected in Step 2 (unless you've disabled it).
5. Import Outlines
    * This step imports the `miHoYo - Outlines` node group, which is found in the `experimental-blender-3.3` folder.
    * Select the `miHoYo - Outlines.blend` file.
6. Setup Outlines (Geometry Nodes)
    * This step creates and sets up the Outlines (Geometry Nodes modifier)
    * Naming Convention of Geometry Nodes: `GeometryNodes {Mesh Name}`
    * No selection needed.
7. Import Lightmaps for Outlines
    * This step imports Lightmap textures and assigns them to to materials.
    * Yes, this tool also handle special exceptions for characters like: `Yelan`, `Collei` and `Rosaria` who may have their `Dress` set to `Hair` instead of the usual `Body`.
    * **This step uses the cache** so you do not need to select a folder. It uses what was selected in Step 2 or Step 4 (unless you've disabled them).
8. Import Material Data
    * This step imports JSON files containing material data with useful information for shader accuracy, such as specular colors, metalmap scale, metallic colors, outline colors, shininess values, etc.
    * Select the JSON files with the material data (Ctrl + Click or Shift + Click).
9. Fix Mouth Outlines **[Disabled by Default]**
    * This step "fixes" outlines on the mouth (Face) by assigning a Camera to the geometry node and setting Depth Offset. You will likely need to manually change the Depth Offset depending on your scene.
    * This step may not be needed if you use BetterFBX to import your model (to be confirmed).


~Mken
