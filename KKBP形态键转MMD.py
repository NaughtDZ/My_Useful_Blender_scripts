#脚本的形态键转换局限，源于此脚本用于KKBP导出FBX后经由Unity转换VRM到PMX格式的mmd模型
#正在尝试制作第二种脚本用于直接将KKBP导入的模型转换成mmd可用模型

import bpy

def mouth_a(obj):
    keys = obj.data.shape_keys.key_blocks
    # 设置原有形态键
    keys["KK Mouth_a_small_op"].value = 1
    bpy.context.view_layer.update()
    # 基于 形态键变形创建新的形态键
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="あ"
    keys["あ"].value = 0

    # 将原有形态键的值恢复到 0
    keys["KK Mouth_a_small_op"].value = 0
    bpy.context.view_layer.update()


def mouth_e(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Mouth_e_small_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="い"
    keys["い"].value = 0

    
    keys["KK Mouth_e_small_op"].value = 0
    bpy.context.view_layer.update()
    


def mouth_i(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Mouth_i_small_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="え"
    keys["え"].value = 0

    
    keys["KK Mouth_i_small_op"].value = 0
    bpy.context.view_layer.update()

def mouth_o(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Mouth_o_small_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="お"
    keys["お"].value = 0

    
    keys["KK Mouth_o_small_op"].value = 0
    bpy.context.view_layer.update()

def mouth_u(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Mouth_u_small_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="う"
    keys["う"].value = 0

    
    keys["KK Mouth_u_small_op"].value = 0
    bpy.context.view_layer.update()

def mouth_a2(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Mouth_a_big_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="あ２"
    keys["あ２"].value = 0

    
    keys["KK Mouth_a_big_op"].value = 0
    bpy.context.view_layer.update()

def mouth_en(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Mouth_chewing_cl"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="ん"
    keys["ん"].value = 0

    
    keys["KK Mouth_chewing_cl"].value = 0
    bpy.context.view_layer.update()

def mouth_triangle(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Mouth_triangle_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="▲"
    keys["▲"].value = 0

    
    keys["KK Mouth_triangle_op"].value = 0
    bpy.context.view_layer.update()

def mouth_AMouth(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Mouth_displeased_cl"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="∧"
    keys["∧"].value = 0

    
    keys["KK Mouth_displeased_cl"].value = 0
    bpy.context.view_layer.update()

def mouth_SquareMouth(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Mouth_eating_2_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="□"
    keys["□"].value = 0

    
    keys["KK Mouth_eating_2_op"].value = 0
    bpy.context.view_layer.update()

def mouth_grinA(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Mouth_cartoon_mouth_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="ワ"
    keys["ワ"].value = 0

    
    keys["KK Mouth_cartoon_mouth_op"].value = 0
    bpy.context.view_layer.update()

def mouth_nekoCL(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Mouth_neko_cl"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="ω"
    keys["ω"].value = 0

    
    keys["KK Mouth_neko_cl"].value = 0
    bpy.context.view_layer.update()

def mouth_nekoOP(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Mouth_neko_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="ω□"
    keys["ω□"].value = 0

    
    keys["KK Mouth_neko_op"].value = 0
    bpy.context.view_layer.update()

def mouth_happy_broad(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Mouth_happy_broad_cl"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="にやり"
    keys["にやり"].value = 0

    
    keys["KK Mouth_happy_broad_cl"].value = 0
    bpy.context.view_layer.update()

def mouth_tongue(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Mouth_lick_cl"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="ぺろっ"
    keys["ぺろっ"].value = 0

    
    keys["KK Mouth_lick_cl"].value = 0
    bpy.context.view_layer.update()

def Eyebrows_serious(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Eyebrows_shocked_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="真面目"
    keys["真面目"].value = 0

    
    keys["KK Eyebrows_shocked_op"].value = 0
    bpy.context.view_layer.update()

def Eyebrows_sad(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Eyebrows_worried_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="困る"
    keys["困る"].value = 0

    
    keys["KK Eyebrows_worried_op"].value = 0
    bpy.context.view_layer.update()

def Eyebrows_angry(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Eyebrows_angry_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="怒り"
    keys["怒り"].value = 0

    
    keys["KK Eyebrows_angry_op"].value = 0
    bpy.context.view_layer.update()

def Eyes_close(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Eyes_default_cl"].value = 0.5

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="まばたき"
    keys["まばたき"].value = 0

    
    keys["KK Eyes_default_cl"].value = 0
    bpy.context.view_layer.update()

def Eyes_smile_cl(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Eyes_smile_cl"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="笑い"
    keys["笑い"].value = 0

    
    keys["KK Eyes_smile_cl"].value = 0
    bpy.context.view_layer.update()
    
def Eyes_squeeze_left(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Eyes_squeeze_left_op"].value = 1
   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="ウィンク"
    keys["ウィンク"].value = 0
    
    keys["KK Eyes_squeeze_left_op"].value = 0
    bpy.context.view_layer.update()
    
def Eyes_squeeze_right(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Eyes_squeeze_right_op"].value = 1
   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="ウィンク右"
    keys["ウィンク右"].value = 0

    
    keys["KK Eyes_squeeze_right_op"].value = 0
    bpy.context.view_layer.update()

def Eyes_squeeze_left_2(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Eyes_squeeze_left_2_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="ウィンク２"
    keys["ウィンク２"].value = 0

    
    keys["KK Eyes_squeeze_left_2_op"].value = 0
    bpy.context.view_layer.update()

def Eyes_squeeze_right_2(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Eyes_squeeze_right_2_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="ウィンク２右"
    keys["ウィンク２右"].value = 0

    
    keys["KK Eyes_squeeze_right_2_op"].value = 0
    bpy.context.view_layer.update()

def Eyes_bored(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Eyes_bored_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="なごみ"
    keys["なごみ"].value = 0

    
    keys["KK Eyes_bored_op"].value = 0
    bpy.context.view_layer.update()

def Eyes_impatient(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Eyes_impatient_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="びっくり"
    keys["びっくり"].value = 0

    
    keys["KK Eyes_impatient_op"].value = 0
    bpy.context.view_layer.update()

def Eyes_dejected(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Eyes_dejected_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="じと目"
    keys["じと目"].value = 0

    
    keys["KK Eyes_dejected_op"].value = 0
    bpy.context.view_layer.update()

def Eyes_small(obj):
    keys = obj.data.shape_keys.key_blocks
    keys["KK Eyes_hate_op"].value = 1

   
    bpy.ops.object.shape_key_add(from_mix=True)
    keys[-1].name ="瞳小"
    keys["瞳小"].value = 0

    
    keys["KK Eyes_hate_op"].value = 0
    bpy.context.view_layer.update()

# 主程序
def main():
    # 获取活动对象
    obj = bpy.context.active_object

    # 确保对象是网格类型并且具有形态键
    if obj and obj.type == 'MESH' and obj.data.shape_keys:
        # 调用函数进行多次操作
        mouth_a(obj)
        mouth_e(obj)
        mouth_i(obj)
        mouth_o(obj)
        mouth_u(obj)
        mouth_a2(obj)
        mouth_en(obj)
        mouth_triangle(obj)
        mouth_AMouth(obj)
        mouth_SquareMouth(obj)
        mouth_grinA(obj)
        mouth_nekoCL(obj)
        mouth_nekoOP(obj)
        mouth_happy_broad(obj)
        mouth_tongue(obj)
        Eyebrows_serious(obj)
        Eyebrows_sad(obj)
        Eyebrows_angry(obj)
        Eyes_close(obj)
        Eyes_smile_cl(obj)
        Eyes_squeeze_left(obj)
        Eyes_squeeze_right(obj)
        Eyes_squeeze_left_2(obj)
        Eyes_squeeze_right_2(obj)
        Eyes_bored(obj)
        Eyes_impatient(obj)
        Eyes_dejected(obj)
        Eyes_small(obj)
    else:
        print("活动对象不是网格或没有形态键")

# 执行主程序
main()


'''
备用项目，混合形态键
def mix_shape_keys(obj, key1_name, key1_value, key2_name, key2_value, new_key_name):
    """
    混合两个形态键并创建一个新的形态键
    
    参数:
    obj -- 目标对象
    key1_name -- 第一个形态键的名称
    key1_value -- 第一个形态键的值
    key2_name -- 第二个形态键的名称
    key2_value -- 第二个形态键的值
    new_key_name -- 新创建的形态键名称
    """
    # 获取形态键列表
    keys = obj.data.shape_keys.key_blocks

    # 设置形态键值
    if key1_name in keys and key2_name in keys:
        keys[key1_name].value = key1_value
        keys[key2_name].value = key2_value

        # 更新对象形状以反映新的形态键值
        bpy.context.view_layer.update()

        # 创建新的形态键
        bpy.ops.object.shape_key_add(from_mix=True)
        keys[-1].name = new_key_name

        # 恢复形态键值
        keys[key1_name].value = 0
        keys[key2_name].value = 0

        # 更新对象形状以反映复原的形态键值
        bpy.context.view_layer.update()
    else:
        print(f"形态键 {key1_name} 或 {key2_name} 不存在")
'''
