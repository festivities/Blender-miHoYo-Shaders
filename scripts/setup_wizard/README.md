# miHoYo Shaders - Setup Wizard Tool

> You should view this on Github or some other Markdown reader if you aren't!

The goal of this tool is to streamline the character setup process. Whether it's importing the materials, importing the character model, setting up the outlines (geometry nodes) or configuring the outline colors to be game accurate, this tool has got it all! Your one-stop-shop for setting up your characters in Blender!

## Table of Contents
1. [Quick Start Guide](#quick-start-guide)
2. [How to Disable Components](#how-to-disable-components---important)
3. [Features/Components](#featurescomponents)
4. [Steps (Detailed Guide)](#steps-detailed-guide)
5. [Development Roadmap/Future Features](#development-roadmap--future-features)
6. ["Tested" Character Models](#tested-character-models)
7. [Credits](#credits)

## Quick Start Guide
1. Open Blender (new file or one with no models)
2. Switch to Scripting
3. Open `genshin_setup_wizard.py`
4. Run the script
5. Hit F3 and type `Genshin`
6. Select the option saying `file.genshin_setup_wizard > Genshin: Setup Wizard - Select Festivity's Shader Folder`
7. Select the root/base folder with Festivity's Shaders
    * Double click to navigate inside the folder to select it, do not select a specific file inside!
    * Ex. My shaders are in a folder called `Blender-miHoYo-Shaders`
8. Select the folder with the character model and textures (lightmaps, diffuses, etc.)
9. Select the `miHoYo - Outlines.blend` file located in the `experimental-blender-3.3` folder
10. Select the material data JSON files for the outlines
    * Shift+Click or Ctrl+Click the JSON files that you want to use (normally all of them)

> **Do you use BetterFBX? Don't want to use FBX's standard import?** <br>
> No problem! Read the section just below on how to disable the Import Character Model component.

## How to Disable Components - Important!
This tool is broken up into many different components. The `config.json` file can be used to enable or disable steps depending on your workflow.

Example:
```
    "1": {
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
* The cache (`cache.json.tmp`) is used to "save" your previous choice for a future step that uses the same folder (ex. character model, textures and outline lightmaps). It gets overwritten each time you run the Setup Wizard and is purely a temporary file.


### Other Notes:
* The `component_name` should NOT be modified. This is how the Setup Wizard identifies and triggers the next component.
* Metadata is simply there to help provide human readable information and what each component requires (what should be selected on the file explorer window).

## Features/Components

> Note: Ideally these steps won't change too much once this releases! Sorry in advance if they do!

0. Setup Wizard
1. Import Character Model
2. Delete Empties
3. Import Materials
4. Replace/Re-Assign Default Character Model Materials (and rename)
5. Import Character Textures
6. Import `miHoYo - Outlines`
7. Setup Outlines (Geometry Nodes)
8. Import Lightmaps for Outlines
9. Import Material Data
10. Fix Mouth Outlines - **[Disabled by Default]**
11. Delete Specific Objects
12. Make Character Upright
13. Set Color Management to 'Standard'
14. Setup Head Driver


## Steps (Detailed Guide)

> Note: Ideally these steps won't change too much once this releases! Sorry in advance if they do!

0. Setup Wizard
    * This step starts the Setup Wizard process. It also is **very important** for setting up the Python paths so that the scripts can import dependencies and other scripts.
    * If you are running into an error about `invoke_next_step`, this is likely your issue. You only need to run this step for the Setup Wizard and then you can close out of the File Explorer window.
    * Select the root folder that contains Festivity's Shaders
        * Cache not enabled in this step in case you run it only to set up your `sys.path`/Python path)
1. Import Character Model
    * This step will: 
        * Import the character model which should be a .fbx file
        * Hide EffectMesh (gets deleted in a later step) and EyeStar
        * Add 'UV1' UV Map to ALL meshes (I think the important one is just Body though?)
        * Resets the location and rotation bones in pose mode and sets the armature into an A-pose (this is is done because we import with `force_connect_children`)
    * Select the folder that contains the character model and textures. **It is assumed that the textures for the character are also in this folder.**
2. Delete Empties
    * This step deletes Empty type objects in the scene
    * No selection needed.
3. Import Materials
    * This step imports `miHoYo - Genshin Hair`, `miHoYo - Genshin Face`, `miHoYo - Genshin Body` and `miHoYo - Genshin Outlines`.
    * Select the root folder that contains Festivity's Shaders.
4. Replace Default Character Model Materials (and rename)
    * This step replaces/re-assigns the default character model materials to the shader's materials.
    * Naming Convention of Genshin Materials (and their Shader nodes): `miHoYo - Genshin {Body Part}` 
        * `{Body Part}` can be `Hair`, `Body`, `Dress`, `Dress1`, `Dress2`, etc.
    * Yes, this tool also handles special exceptions for characters like: `Yelan`, `Collei` and `Rosaria` who may have their `Dress` set to `Hair` instead of the usual `Body`.
    * Select the folder that contains the character model and textures. **It is assumed that the textures for the character are also in this folder.** (Needed purely to get the character name)
5. Import Character Textures
    * This step imports the character textures and assigns them to the materials imported in Step `Import Materials`.
    * Yes, this tool also handles special exceptions for characters like: `Yelan`, `Collei` and `Rosaria` who may have their `Dress` set to `Hair` instead of the usual `Body`.
    * **This step uses the cache** so you do not need to select a folder. It uses what was selected in Step `Import Character Model` (unless you've disabled it).
6. Import `miHoYo - Outlines`
    * This step imports the `miHoYo - Outlines` node group, which is found in the `experimental-blender-3.3` folder.
    * Select the `miHoYo - Outlines.blend` file.
7. Setup Outlines (Geometry Nodes)
    * This step creates and sets up the Outlines (Geometry Nodes modifier)
    * Naming Convention of Geometry Nodes: `GeometryNodes {Mesh Name}`
        * {Mesh Name} can be `Body`, `Face`, `Face_Eye`, `Brow` (`Face_Eye` and `Brow` don't really get used though and `Face_Eye` has Outline Thickness set to 0.0 by default)
    * Naming Convention of Outline Materials: `miHoYo - Genshin {Body Part} Outlines`
        * `{Body Part}` can be `Hair`, `Body`, `Dress`, `Dress1`, `Dress2`, etc.
    * No selection needed.
8. Import Lightmaps for Outlines
    * This step imports Lightmap textures and assigns them to to materials.
    * Yes, this tool also handles special exceptions for characters like: `Yelan`, `Collei` and `Rosaria` who may have their `Dress` set to `Hair` instead of the usual `Body`.
    * **This step uses the cache** so you do not need to select a folder. It uses what was selected in Step `Import Character Model` or Step `Import Character Textures` (unless you've disabled them).
9. Import Material Data
    * This step imports JSON files containing material data with useful information for shader accuracy, such as specular colors, metalmap scale, metallic colors, outline colors, shininess values, etc.
    * Select the JSON files with the material data (Ctrl + Click or Shift + Click).
10. Fix Mouth Outlines - **[Disabled by Default]**
    * This step "fixes" outlines on the mouth (Face) by assigning a Camera to the geometry node and setting Depth Offset. You will likely need to manually change the Depth Offset depending on your scene.
    * This step may not be needed if you use BetterFBX to import your model (to be confirmed).
11. Delete Specific Objects
    * This step deletes specific object(s) which is only EffectMesh at this time.
    * No selection needed.
12. Make Character Upright
    * This step will reset the rotation and scale of the character armature and set the character armature to 90 degrees on the x-axis (standing upright).
    * No selection needed.
13. Set Color Management to 'Standard'
    * This step will set the Color Management to Standard (normally Filmic)
    * No selection needed.
14. Setup Head Driver
    * This step will setup the Head Driver constraint so that face shadows work
    * No selection needed.

## Development Roadmap / Future Features
### Features
- [X] Head Driver Setup
- [X] Make model upright if not upright (?)
- [X] ~~Scale up x100~~ Reset Scale (scaled to 1.0)
- [ ] Character Ramp Type Mapping (automatically plug correct Body Ramp Type from Global Material Properties)
    - Requires knowing all characters who have a different the Body Ramp Type than the default
- [X] BetterFBX Support/Fix UV map imports (only one UV map is imported)
    - Created UV1 UV map which allows for underskirt textures (Zhongli, Lumine, etc.)
    - No BetterFBX support still at this time though... 
- [X] Color Management Filmic -> Standard
### Refactoring
- [X] Refactor Material Assignment Mapping (externalize/centralize it to one locaiton)
- [ ] Refactor Import Outline Lightmaps component
- [ ] Refactor config.json from a dictionary to a List of dictionaries?
### Misc.
- [X] Crude design diagram depicting how this tool and the components interact and work

![alt text](https://user-images.githubusercontent.com/8632035/183316362-8a47f471-0fa4-4a3d-8e17-ea2c2a9a852e.png)

## "Tested" Character Models
The models below should not throw errors when running the Setup Wizard.
- Amber
- Alhaitham
- Collei
- Dori
- Hu Tao
- Kamisato Ayato
- Keqing
- Lumine
- Nahida
- Nilou
- Rosaria
- Tighnari
- Yelan

#

## Credits

Thanks to all those who helped answer the questions I had while building out this tool and learning about Blender.
<br>
Shoutout to @Festivity, @TheyCallMeSpy, @Sultana, @M4urlcl0 and @Modder4869!

Cheers and Happy Blending,

~Mken
