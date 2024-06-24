import bpy

# 获取活动对象
obj = bpy.context.object

if obj and obj.data.shape_keys:
    # 获取形态键块
    shape_key_block = obj.data.shape_keys.key_blocks
    
    # 找出所有后缀为 ".002" 的形态键名称
    shape_keys_to_delete = [key.name for key in shape_key_block if key.name.endswith(".001")]
    
    # 反转列表顺序，以避免删除时索引改变的问题
    for key_name in sorted(shape_keys_to_delete, reverse=True):
        if key_name in shape_key_block:
            # 删除形态键
            obj.shape_key_remove(shape_key_block[key_name])
    print(f"Deleted shape keys: {shape_keys_to_delete}")
else:
    print("No shape keys found on the active object.")
