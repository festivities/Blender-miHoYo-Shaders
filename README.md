# miHoYo Shaders for Blender 3.0 and above

## Preview
![Preview](https://pbs.twimg.com/media/FFG9XFZVIAEGbax?format=jpg)
![Preview, horrible quality I know](https://github.com/Festivize/Blender-miHoYo-Shaders/blob/main/genshin-preview/genshin-preview1.gif)
![Preview, horrible quality I know](https://github.com/Festivize/Blender-miHoYo-Shaders/blob/main/genshin-preview/genshin-preview2.gif)

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

## Special thanks
This wouldn't be possible if it weren't for ArcSys, [Aerthas Veras](https://github.com/Aerthas/), [Manashiku](https://github.com/Manashiku/), the folks over at 知乎专栏 and many more I simply can't cite who choose to share their knowledge and open-source their own shaders. For that, I'd like to give back to the community with what I've learned. Enjoy! I hope you learn a thing or two.
