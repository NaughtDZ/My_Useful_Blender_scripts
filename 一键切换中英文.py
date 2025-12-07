# Blender 5.0+ 可用（也兼容 4.2~4.3）
# 功能: 一键切换 Blender UI 语言（中文 ↔ 英文）
# 沟槽的Blender5.0了还在用全局字典做翻译，各种垃圾抽象翻译云里雾里严重导致学习成本极大，网上优质的教学又都是英文的

bl_info = {
    "name": "一键中英文切换",
    "author": "Grok",
    "version": (1, 3),
    "blender": (4, 2, 0),
    "location": "顶部状态栏（可见性/渲染通行证旁边）",
    "description": "点击按钮在中文和英文界面之间快速切换",
    "category": "界面",
}

import bpy
from bpy.types import Operator

# 记录当前是哪种语言
def get_current_lang():
    return bpy.context.preferences.view.language

def is_chinese():
    lang = get_current_lang()
    return lang == "zh_CN" or lang == "zh_HANS"

class VIEW3D_OT_toggle_language(Operator):
    bl_idname = "wm.toggle_language"
    bl_label = "切换语言"
    bl_description = "点击切换 Blender 界面语言：中文 ↔ English"
    bl_options = {'REGISTER'}

    def execute(self, context):
        prefs = context.preferences
        view = prefs.view

        if is_chinese():
            # 切到英文
            view.language = "en_US"
            view.use_translate_tooltips = False
            view.use_translate_interface = True  # 仍然启用翻译系统，只是语言包是英文
            self.report({'INFO'}, "Language → English")
        else:
            # 切到简体中文
            view.language = "zh_HANS"          # Blender 4.2+ 推荐写法
            view.use_translate_tooltips = True
            view.use_translate_interface = True
            self.report({'INFO'}, "语言 → 简体中文")

        # 强制刷新界面（很重要！）
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}

# 把按钮画在状态栏最右侧（和可见性、着色方式同一行）
def draw_language_button(self, context):
    layout = self.layout
    # 放一个分隔符让按钮靠右一些，看起来更舒服
    layout.separator_spacer()
    # 小地球图标（不带边框，看起来更干净）
    layout.operator("wm.toggle_language", text="", icon='WORLD', emboss=False)

# 注册时把按钮加到状态栏
def register():
    bpy.utils.register_class(VIEW3D_OT_toggle_language)
    
    # Blender 5.0 状态栏是 TOPBAR_HT_upper_bar
    # 老版本是 STATUSBAR_HT_header（但5.0基本不用了）
    # 我们兼容两者，但优先 TOPBAR_HT_upper_bar
    try:
        bpy.types.TOPBAR_HT_upper_bar.append(draw_language_button)
    except AttributeError:
        pass
    try:
        bpy.types.STATUSBAR_HT_header.append(draw_language_button)
    except AttributeError:
        pass

def unregister():
    bpy.utils.unregister_class(VIEW3D_OT_toggle_language)
    
    try:
        bpy.types.TOPBAR_HT_upper_bar.remove(draw_language_button)
    except:
        pass
    try:
        bpy.types.STATUSBAR_HT_header.remove(draw_language_button)
    except:
        pass

if __name__ == "__main__":
    register()
