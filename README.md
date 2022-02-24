# miHoYo Shaders for Blender 3.0 and above

## Preview
![Preview](https://pbs.twimg.com/media/FMHJjhOUYAAvPnR?format=jpg)

![Preview](https://pbs.twimg.com/media/FFG9XFZVIAEGbax?format=jpg)

https://user-images.githubusercontent.com/77230051/153713701-e6e796d6-b65a-42b1-a04d-e3a03f99f54b.mp4

https://user-images.githubusercontent.com/77230051/153380331-7b219a26-f627-4f09-ba1f-8bb4491474cb.mp4

## Usage
1. Download a release [here](https://github.com/Festivize/Blender-miHoYo-Shaders/releases).
2. In a new project with your desired character mesh, append whatever materials the .blend file you downloaded will contain.
3. Replace the original materials of the mesh with the materials from the .blend file you just appended.
4. Use this [script](https://github.com/Festivize/Blender-miHoYo-Shaders/tree/main/scripts/genshin-import.py) to import your textures.
5. Constrain the empty object named *Head Driver* to the head bone of your character with a **Child Of** constraint.
6. In the *Global Material Properties* panel, you may wonder what the Body Y and Hair Y values are supposed to be - those correspond to the ramp textures. Refer to this little infographic I [made](https://i.imgur.com/r7BqTBV.png).
7. I'll be making a video guide soon. If anyone wants to help out, that'd be appreciated.

## Milestones
These shaders aren't meant to be 100% accurate - in fact they will most likely never be until someone blesses us with the decompiled shader code. Until then, what I only aim for is to replicate the in-game looks to the best of my ability.

### Genshin Impact
- [x] Ramp texture implementation **(done thanks to [Manashiku](https://github.com/Manashiku/MMDGenshin/))**
- [x] Face shading
- [x] Metallic matcap function
- [x] Specular function
- [x] Custom light/shadow settings for creative freedom
- [x] Stable release
- [ ] Constant width rim lighting *(until Blender implements real-time compositing/screen shaders, I don't see this feature happening anytime soon, for now have a simple NdotV rim light)*
- [ ] Constant width outlines *(it's actually possible with Geometry Nodes, but it's far too non-intuitive for the average user to set up, waiting for Blender to implement actual vertex shaders)*
- [x] Outline material

### Honkai: Star Rail
- [x] Ramp texture implementation **(done thanks to [Manashiku](https://github.com/Manashiku/MMDGenshin/))**
- [x] Face shading
- [x] Specular function
- [x] Custom light/shadow settings for creative freedom
- [ ] Stable release
- [ ] Constant width rim lighting *(see above)*
- [ ] Constant width outlines *(see above)*
- [x] Outline material

### Honkai Impact 3rd
- [ ] Learn how to datamine assets from the game LOL someone please make a tool

## Support
- [Discord server](https://discord.gg/Sp9vDCvWRW)
- [Twitter](https://twitter.com/Festivizing)

## Rules
- The [GPL-3.0 License](https://github.com/Festivize/Blender-miHoYo-Shaders/blob/main/LICENSE) applies.
- If you use this shader as is in renders, animations or any form of medium that does not directly modify the shader, I'd appreciate being credited - **you don't have to do it though.**
- If you use this shader as the main reference for your own shader, please give credit where it's due.
- In compliance with the license, you are free to redistribute the files as long as you attach a link to the source repository.

## Special thanks
This wouldn't be possible if it weren't for ArcSys, [Aerthas Veras](https://github.com/Aerthas/), [Manashiku](https://github.com/Manashiku/), the folks over at 知乎专栏 and many more I simply can't cite who choose to share their knowledge and open-source their own shaders. For that, I'd like to give back to the community with what I've learned. A huge thanks to Zekium from Discord as well for contributing the script to automate the importing of textures. With that said, I hope you learn a thing or two. Enjoy!

## Disclaimer

While the shaders are developed primarily for datamined assets, this repository does not endorse datamining whatsoever and will never directly provide the assets nor tools in extracting from game files.