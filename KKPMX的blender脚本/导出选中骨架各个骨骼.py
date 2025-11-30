# -*- coding: utf-8 -*-
#blender 5.0验证通过
# 导出骨架骨骼名称（层级结构）—— Blender 5.0 最终稳定版
# 直接全选复制 → 新建文本块 → Run Script 即可永久使用
#运行脚本后会功能在N面板的工具tool那里

import bpy
import os
from bpy.props import StringProperty, BoolProperty

bl_info = {
    "name": "导出骨骼名称（层级）",
    "author": "Grok",
    "version": (2, 0),
    "blender": (4, 2, 0),
    "location": "3D视图 → N面板 → Tool → 导出骨骼名称",
    "description": "一键导出当前骨架全部或选中骨骼的层级名称",
    "category": "Armature",
}

def get_hierarchy_bones(arm_obj, selected_only=True):
    bones = []

    # 获取当前模式下的骨骼列表
    if arm_obj.mode == 'EDIT':
        all_bones = arm_obj.data.edit_bones
        src = [b for b in all_bones if b.select] if selected_only else all_bones
    elif arm_obj.mode == 'POSE':
        src = [p.bone for p in arm_obj.pose.bones if p.bone.select] if selected_only else arm_obj.data.bones
    else:
        src = arm_obj.data.bones

    if not src:
        return bones

    def add(bone, depth=0):
        if not bone:
            return
        bones.append((bone.name, depth))
        for child in getattr(bone, "children", []):
            add(child, depth + 1)

    roots = [b for b in src if not b.parent]
    for root in roots:
        add(root, 0)

    return bones


class ARMATURE_OT_export_bone_names(bpy.types.Operator):
    bl_idname = "armature.export_bone_names"
    bl_label = "导出骨骼名称"
    bl_description = "导出骨骼名称到文本文件"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: StringProperty(subtype='FILE_PATH')
    selected_only: BoolProperty(default=True)

    def invoke(self, context, event):
        arm = context.active_object
        name = arm.name if arm and arm.type == 'ARMATURE' else "bones"
        self.filepath = bpy.path.ensure_ext(f"{name}_bones.txt", ".txt")
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        arm = context.active_object
        if not arm or arm.type != 'ARMATURE':
            self.report({'ERROR'}, "请选中一个骨架（Armature）对象！")
            return {'CANCELLED'}

        bone_list = get_hierarchy_bones(arm, self.selected_only)

        if not bone_list:
            self.report({'WARNING'}, "没有找到骨骼！请检查是否在 Pose/Edit 模式下选中了骨骼")
            return {'CANCELLED'}

        lines = [
            f"# Armature: {arm.name}",
            f"# 骨骼数量: {len(bone_list)}",
            f"# 模式: {arm.mode}   帧: {context.scene.frame_current}",
            "",
        ]
        for name, depth in bone_list:
            lines.append("    " * depth + name)

        content = "\n".join(lines) + "\n"

        # 写入文件
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                f.write(content)
            self.report({'INFO'}, f"成功导出 {len(bone_list)} 个骨骼！")
        except Exception as e:
            self.report({'ERROR'}, f"写入失败: {e}")  # 修复的这行！
            return {'CANCELLED'}

        # 在 Blender 内创建同名文本块，方便直接复制
        txt_name = os.path.basename(self.filepath)
        if txt_name in bpy.data.texts:
            bpy.data.texts.remove(bpy.data.texts[txt_name])
        txt = bpy.data.texts.new(txt_name)
        txt.write(content)

        return {'FINISHED'}


# 面板
class VIEW3D_PT_export_bone_names(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"
    bl_label = "导出骨骼名称"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        if obj and obj.type == 'ARMATURE':
            col = layout.column(align=True)
            op = col.operator("armature.export_bone_names", text="导出全部骨骼", icon='ARMATURE_DATA')
            op.selected_only = False
            op = col.operator("armature.export_bone_names", text="仅导出选中骨骼", icon='BONE_DATA')
            op.selected_only = True
        else:
            layout.label(text="请先选中一个骨架", icon='INFO')


def register():
    bpy.utils.register_class(ARMATURE_OT_export_bone_names)
    bpy.utils.register_class(VIEW3D_PT_export_bone_names)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_export_bone_names)
    bpy.utils.unregister_class(ARMATURE_OT_export_bone_names)

if __name__ == "__main__":
    register()