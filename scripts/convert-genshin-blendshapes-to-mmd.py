import bpy

# set selected object as active and call its shape keys
obj = bpy.context.object
shape_keys = obj.data.shape_keys.key_blocks

# for Brow
for brow_key in shape_keys:
    brow_key.name = brow_key.name.replace("Brow_Trouble_L", "困る左")
    brow_key.name = brow_key.name.replace("Brow_Trouble_R", "困る右")
    brow_key.name = brow_key.name.replace("Brow_Smily_L", "にこり左")
    brow_key.name = brow_key.name.replace("Brow_Smily_R", "にこり右")
    brow_key.name = brow_key.name.replace("Brow_Angry_L", "怒り左")
    brow_key.name = brow_key.name.replace("Brow_Angry_R", "怒り右")
    brow_key.name = brow_key.name.replace("Brow_Shy_L", "恥ずかしい左")
    brow_key.name = brow_key.name.replace("Brow_Shy_R", "恥ずかしい右")
    brow_key.name = brow_key.name.replace("Brow_Up_L", "上左")
    brow_key.name = brow_key.name.replace("Brow_Up_R", "上右")
    brow_key.name = brow_key.name.replace("Brow_Down_L", "下左")
    brow_key.name = brow_key.name.replace("Brow_Down_R", "下右")
    brow_key.name = brow_key.name.replace("Brow_Squeeze_L", "に近い左")
    brow_key.name = brow_key.name.replace("Brow_Squeeze_R", "に近い右")

# for Face
for mouth_key in shape_keys:
    mouth_key.name = mouth_key.name.replace("Mouth_A01", "あ")
    mouth_key.name = mouth_key.name.replace("Mouth_Open01", "え")
    mouth_key.name = mouth_key.name.replace("Mouth_Smile01", "にやり")
    mouth_key.name = mouth_key.name.replace("Mouth_Smile02", "ワ")
    mouth_key.name = mouth_key.name.replace("Mouth_Angry01", "ん")
    mouth_key.name = mouth_key.name.replace("Mouth_Angry02", "い１")
    mouth_key.name = mouth_key.name.replace("Mouth_Angry03", "い２")
    mouth_key.name = mouth_key.name.replace("Mouth_Fury01", "あ２")
    mouth_key.name = mouth_key.name.replace("Mouth_Doya01", "にやり２")
    mouth_key.name = mouth_key.name.replace("Mouth_Doya02", "にやり３")
    mouth_key.name = mouth_key.name.replace("Mouth_Neko01", "ω")
    mouth_key.name = mouth_key.name.replace("Mouth_Pero01", "てへぺろ")
    mouth_key.name = mouth_key.name.replace("Mouth_Pero02", "ぺろっ")
    mouth_key.name = mouth_key.name.replace("Mouth_Line01", "口横広げ")
    mouth_key.name = mouth_key.name.replace("Mouth_Line02", "口横狭め")
    mouth_key.name = mouth_key.name.replace("Mouth_BigTongue01", "舌広げ")

# for Face_Eye
for eye_key in shape_keys:
    eye_key.name = eye_key.name.replace("Eye_WinkA_L", "ウィンク")
    eye_key.name = eye_key.name.replace("Eye_WinkA_R", "ウィンク右")
    eye_key.name = eye_key.name.replace("Eye_WinkB_L", "ウィンク２")
    eye_key.name = eye_key.name.replace("Eye_WinkB_R", "ｳｨﾝｸ２右")
    eye_key.name = eye_key.name.replace("Eye_WinkC_L", "なごみ左")
    eye_key.name = eye_key.name.replace("Eye_WinkC_R", "なごみ右")
    eye_key.name = eye_key.name.replace("Eye_Ha", "びっくり")
    eye_key.name = eye_key.name.replace("Eye_Jito", "じと目")
    eye_key.name = eye_key.name.replace("Eye_Wail", "喜び")
    eye_key.name = eye_key.name.replace("Eye_Hostility", "怒り目")
    eye_key.name = eye_key.name.replace("Eye_Tired", "ジト目")
    eye_key.name = eye_key.name.replace("Eye_WUp", "眼角上")
    eye_key.name = eye_key.name.replace("Eye_WDown", "眼角下")
    eye_key.name = eye_key.name.replace("Eye_Lowereyelid", "下眼上")