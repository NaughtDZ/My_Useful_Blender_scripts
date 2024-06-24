import bpy
import math
import mathutils

# 获取所有合集
collections = bpy.data.collections

# 定义行数
x_count = 5  # 每行的合集数

# 计算总合集数
total_collections = len(collections)

# 计算列数
y_count = math.ceil(total_collections / x_count)

# 定义间隔距离
x_spacing = 50.0
y_spacing = 50.0

# 起始位置
start_x = 0.0
start_y = 0.0

# 当前合集索引
index = 0

# 遍历合集并设置位置
for y in range(y_count):
    for x in range(x_count):
        if index >= total_collections:
            break
        
        # 计算当前合集的位置
        x_position = start_x + x * x_spacing
        y_position = start_y + y * y_spacing
        
        # 获取当前合集
        collection = collections[index]
        
        # 选中合集中的所有对象
        bpy.ops.object.select_all(action='DESELECT')  # 取消选择所有对象
        for obj in collection.objects:
            obj.select_set(True)  # 选择合集中的对象
        
        # 获取当前选中的对象
        selected_objects = [obj for obj in bpy.context.selected_objects]
        
        # 计算集合中心
        if selected_objects:
            bpy.context.view_layer.update()  # 确保对象位置是最新的
            collection_center = sum((obj.location for obj in selected_objects), mathutils.Vector()) / len(selected_objects)
        
        # 计算平移向量
        translation_vector = mathutils.Vector((x_position, y_position, 0)) - collection_center
        
        # 平移合集中的所有对象
        bpy.ops.transform.translate(value=translation_vector)
        
        # 移动到下一个合集
        index += 1

print("All collections have been arranged in a grid while preserving relative positions.")
