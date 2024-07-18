import bpy
import bmesh

# 获取当前对象
obj = bpy.context.active_object

# 确保对象在编辑模式下
if obj.mode == 'EDIT':

    # 获取对象的网格数据
    bm = bmesh.from_edit_mesh(obj.data)

    # 取消所有边的选择
    for e in bm.edges:
        e.select = False

    # 选择只有一个邻面的边
    for e in bm.edges:
        if len(e.link_faces) == 1:
            e.select = True

    # 更新编辑网格以显示更改
    bmesh.update_edit_mesh(obj.data)

else:
    print("请确保对象在编辑模式下")

