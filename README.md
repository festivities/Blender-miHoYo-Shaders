# miHoYo Shaders for Blender 3.2 and above

## Preview *(heavily post-processed, will include raw previews soon)*
![Preview](https://pbs.twimg.com/media/FMHJjhOUYAAvPnR?format=jpg)

![Preview](https://pbs.twimg.com/media/FFG9XFZVIAEGbax?format=jpg)

## Tutorial/Overview made by No_Tables *(thank you!)*

[![Tutorial by No_Tables](https://i.imgur.com/ktMusVY.jpg)](https://youtu.be/97G7LqFoTdY)

## Usage
1. Either download a release [here](https://github.com/Festivize/Blender-miHoYo-Shaders/releases), or download from the [source](https://github.com/Festivize/Blender-miHoYo-Shaders/archive/refs/heads/main.zip) for the latest commit.
2. In a new project with your desired character mesh, append whatever materials the .blend file you downloaded will contain.
3. Replace the original materials of the mesh with the materials from the .blend file you just appended.
4. You can either use this [script](https://github.com/Festivize/Blender-miHoYo-Shaders/blob/main/scripts/genshin-import-linear.py) to import your textures, or just import them all one-by-one.
5. Constrain the empty object named *Head Driver* to the head bone of your character with a **Child Of** constraint.
6. In the *Global Material Properties* panel, you may wonder what the Body Y and Hair Y values are supposed to be - those correspond to the ramp textures. Refer to this little infographic I [made](https://i.imgur.com/r7BqTBV.png).
7. A [tutorial](https://youtu.be/97G7LqFoTdY) made by [No_Tables](https://twitter.com/No_Tables) showcases the actual shader without any post-processing, and provides an overview as well.

## Milestones
These shaders aren't meant to be 100% accurate - in fact they will most likely never be until someone blesses us with the decompiled shader code. Until then, what I only aim for is to replicate the in-game looks to the best of my ability.

### Genshin Impact
- [x] Ramp texture implementation **(done thanks to [Manashiku](https://github.com/Manashiku/MMDGenshin/))**
- [x] Face shading
- [x] Metallic matcap function
- [x] Specular function
- [x] Custom light/shadow settings for creative freedom
- [x] Stable release
- [ ] Constant width rim lighting *(I've made a setup based on Ben Ayers' [nodes](https://www.artstation.com/blogs/bjayers/9oOD/blender-npr-recreating-the-genshin-impact-shader) with some improvements,  however as this is nowhere near to how the game even does it, I'll be leaving this unticked for now)*
- [x] Constant width outlines *(currently experimental for Geometry Nodes)*
- [x] Outline material

### Honkai: Star Rail
- [x] Ramp texture implementation **(done thanks to [Manashiku](https://github.com/Manashiku/MMDGenshin/))**
- [x] Face shading
- [x] Specular function
- [x] Custom light/shadow settings for creative freedom
- [ ] Stable release
- [ ] Constant width rim lighting *(see above)*
- [x] Constant width outlines *(see above)*
- [x] Outline material

### Honkai Impact 3rd
- [ ] Learn how to datamine assets from the game LOL someone please make a tool

## Contact
- [Discord server](https://discord.gg/85rP9SpAkF)
- [Twitter](https://twitter.com/Festivizing)

## Rules
- The [GPL-3.0 License](https://github.com/Festivize/Blender-miHoYo-Shaders/blob/main/LICENSE) applies.
- If you use this shader as is in renders, animations or any form of medium that does not directly modify the shader, I'd appreciate being credited - **you don't have to do it though.**
- If you use this shader as the main reference for your own shader, please give credit where it's due.
- In compliance with the license, you are free to redistribute the files as long as you attach a link to the source repository.

## Special thanks
All of this wouldn't be possible if it weren't for:
- Arc System Works
- miHoYo
- [Aerthas Veras](https://github.com/Aerthas/) 
- [Manashiku](https://github.com/Manashiku/)
- The folks over at [知乎专栏](https://zhuanlan.zhihu.com/)
- JTAOO
- Zekium and RumblingRose for some of the handy scripts
- [No_Tables](https://twitter.com/No_Tables) for making an intuitive video on using the shader

For that, I'd like to give back to the community with what I've learned. With that said, I hope you learn a thing or two. Enjoy!

## Disclaimer
While the shaders are developed primarily for datamined assets, this repository does not endorse datamining in any way whatsoever and will never directly provide the assets nor tools in extracting from game files.

## Since you've read this far...
Using this shader is completely **free** if it's not already evident from the license BUT - if and only if you have something to spare and would like to support me, then you can do so on my Ko-fi [here](https://ko-fi.com/festivity). I appreciate every tip and each one motivates me to keep on improving the shader.