# Contributed by RumblingRose - huge thank you!

import bpy

OriginalMesh = bpy.context.active_object.name
bpy.ops.object.duplicate()
NewMesh = bpy.context.active_object.name
for shapekey in bpy.data.objects[OriginalMesh].data.shape_keys.key_blocks:
    DriverAdd = bpy.data.objects[NewMesh].data.shape_keys.key_blocks[shapekey.name].driver_add("value")
    Driver1Variable = DriverAdd.driver.variables.new()
    Driver1Variable.name = "Var1"
    Driver1Variable.type = 'SINGLE_PROP'
    Driver1Target = Driver1Variable.targets[0]
    Driver1Target.id = bpy.data.objects[OriginalMesh]
    Driver1Target.data_path = ('data.shape_keys.key_blocks' + '["' + shapekey.name + '"].value')
    DriverAdd.driver.expression = "Var1"