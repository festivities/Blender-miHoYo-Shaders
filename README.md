# miHoYo Shaders for Blender 3.0 and above

## Preview
![Preview](https://pbs.twimg.com/media/FFG9XFZVIAEGbax?format=jpg)
![Preview, horrible quality I know](https://github.com/Festivize/Blender-miHoYo-Shaders/blob/main/genshin-preview/genshin-preview1.gif)
![Preview, horrible quality I know](https://github.com/Festivize/Blender-miHoYo-Shaders/blob/main/genshin-preview/genshin-preview2.gif)

## Usage
1. Download a release [here](https://github.com/Festivize/Blender-miHoYo-Shaders/releases).
2. In a new project with your desired character mesh, append whatever materials the .blend file you downloaded will contain.
3. Add in the textures - this includes the metallic matcap texture, diffuse textures, lightmaps, etc. **I won't be redistributing them. You can datamine them yourself or ask somewhere else.**
4. Constrain the empty object named *Head Driver* to the head bone of your character with a **Child Of** constraint.
5. I'll be making a video guide soon. If anyone wants to help out, that'd be appreciated.

## Milestones
These shaders aren't meant to be 100% accurate - in fact they will most likely never be until someone blesses us with the decompiled shader code. Until then, what I only aim for is to replicate the in-game looks to the best of my ability.

### Genshin Impact
- [x] Ramp texture implementation **(done thanks to [Manashiku](https://github.com/Manashiku/MMDGenshin/))**
- [x] Face shading
- [x] Metallic matcap function
- [x] Specular function **(done with some inspiration from Aerthas' [ArcSys shader](https://github.com/Aerthas/BLENDER-Arc-System-Works-Shader))**
- [x] Custom light/shadow settings for creative freedom
- [x] Stable release
- [ ] Constant width rim lighting *(until Blender implements real-time compositing/screen shaders, I don't see this feature happening anytime soon, for now have a simple NdotV rim light)*
- [ ] Constant width outlines *(it's actually possible with Geometry Nodes, but it's far too non-intuitive for the average user to set up, waiting for Blender to implement actual vertex shaders)*
- [ ] Outline material *(will do this soon)*

### Honkai: Star Rail
- [x] Ramp texture implementation **(done thanks to [Manashiku](https://github.com/Manashiku/MMDGenshin/))**
- [x] Face shading
- [x] Specular function **(done with some inspiration from Aerthas' [ArcSys shader](https://github.com/Aerthas/BLENDER-Arc-System-Works-Shader))**
- [x] Custom light/shadow settings for creative freedom
- [ ] Stable release
- [ ] Constant width rim lighting *(see above)*
- [ ] Constant width outlines *(see above)*
- [ ] Outline material *(see above)*

### Honkai Impact 3rd
- [ ] Learn how to datamine assets from the game LOL someone please make a tool

## Support
- [Discord server](https://discord.gg/Sp9vDCvWRW)
- [Twitter](https://twitter.com/Festivizing)

## Rules
- If you use this shader in your project, I'd appreciate being credited - **you don't have to do it though.**
- If you use this shader as your main reference, please give credit where its due.
- Please don't redistribute the files, I'd appreciate it more if you linked this GitHub repo instead ^^

## Special thanks
This wouldn't be possible if it weren't for ArcSys, [Aerthas Veras](https://github.com/Aerthas/), [Manashiku](https://github.com/Manashiku/), the folks over at 知乎专栏 and many more I simply can't cite who choose to share their knowledge and open-source their own shaders. For that, I'd like to give back to the community with what I've learned. I hope you learn a thing or two. Enjoy!
