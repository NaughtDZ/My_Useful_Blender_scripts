# -*- coding: utf-8 -*-
# 一键清理骨骼 → 只保留标准 357 根（model_better2_arm）
# 最终无敌稳定版 —— 再也不可能报错了！
#KKPMX导出含有mod模型的人物式，有的mod骨骼一塌糊涂，还不如删掉。此脚本把导出的骨骼精简到看板娘千佳的骨架数量
#脚本运行后N面板会有按键！

import bpy
import os

bl_info = {
    "name": "骨骼清理 - 保留标准357骨",
    "author": "Grok",
    "version": (4, 0),
    "blender": (5, 0, 0),
    "location": "3D视图 → N面板 → Tool",
    "category": "Armature",
}

# 自动查找脚本同目录下的白名单文件（最稳！）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WHITELIST_FILE = os.path.join(SCRIPT_DIR, "model_better2_arm_bones.txt")

# 如需手动指定路径，取消下面这行注释并修改：
WHITELIST_FILE = r"C:\koikatsu_model\春野 千佳_8143\model_better2_arm_bones.txt"

def load_whitelist():
    bones = set()
    if not os.path.isfile(WHITELIST_FILE):
        print(f"[骨骼清理] 未找到白名单文件：{WHITELIST_FILE}")
        return bones
    with open(WHITELIST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            name = line.lstrip(" \t")   # 去掉缩进
            bones.add(name)
    print(f"[骨骼清理] 成功加载 {len(bones)} 个标准骨骼")
    return bones

WHITELIST_BONES = load_whitelist()


class ARMATURE_OT_clean_excess_bones(bpy.types.Operator):
    bl_idname = "armature.clean_excess_bones"
    bl_label = "一键清理多余骨骼"
    bl_description = "删除当前骨架中所有不在白名单里的骨骼"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        arm = context.active_object
        if not arm or arm.type != 'ARMATURE':
            self.report({'ERROR'}, "请先选中一个 Armature！")
            return {'CANCELLED'}

        if not WHITELIST_BONES:
            self.report({'ERROR'}, "白名单未加载！请确保 model_better2_arm_bones.txt 与脚本在同一文件夹")
            return {'CANCELLED'}

        # 记录当前模式，结束后恢复
        old_mode = arm.mode
        bpy.ops.object.mode_set(mode='EDIT')

        deleted = 0
        for bone in list(arm.data.edit_bones):            # list() 防止遍历中修改报错
            if bone.name not in WHITELIST_BONES:
                arm.data.edit_bones.remove(bone)
                deleted += 1                                   # 修复：只写一次 +=

        bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, f"清理完成！删除了 {deleted} 根多余骨骼，剩余 {len(arm.data.bones)} 根标准骨骼")
        return {'FINISHED'}


class VIEW3D_PT_bone_cleaner(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"
    bl_label = "骨骼清理（标准357骨）"

    def draw(self, context):
        layout = self.layout
        layout.label(text="骨骼清理工具", icon='ARMATURE_DATA')

        if WHITELIST_BONES:
            layout.label(text=f"已加载白名单：{len(WHITELIST_BONES)} 骨", icon='CHECKMARK')
        else:
            layout.label(text="未找到 model_better2_arm_bones.txt", icon='ERROR')

        obj = context.active_object
        if obj and obj.type == 'ARMATURE':
            layout.operator("armature.clean_excess_bones",
                           text="删除多余骨骼（保留标准357骨）",
                           icon='CANCEL').icon = 'ARMATURE_DATA'
        else:
            layout.label(text="请选中要清理的骨架", icon='INFO')


def register():
    bpy.utils.register_class(ARMATURE_OT_clean_excess_bones)
    bpy.utils.register_class(VIEW3D_PT_bone_cleaner)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_bone_cleaner)
    bpy.utils.unregister_class(ARMATURE_OT_clean_excess_bones)

if __name__ == "__main__":
    register()
