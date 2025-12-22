import os
import re
from pathlib import Path

# 匹配：两个英文字母 + 至少一个数字 开头
RJ_LIKE_PATTERN = re.compile(r'^[A-Za-z]{2}\d')

def is_valid_folder_name(name):
    return bool(RJ_LIKE_PATTERN.match(name))

def swap_folders_by_pattern(root_dir_str):
    root = Path(root_dir_str).resolve()
    if not root.is_dir():
        print(f"❌ 根目录无效: {root}")
        return

    for lv1_path in root.iterdir():
        if not lv1_path.is_dir():
            continue

        # 查找第一个符合 "两个字母+数字" 开头的子目录
        lv2_path = None
        for item in lv1_path.iterdir():
            if item.is_dir() and is_valid_folder_name(item.name):
                lv2_path = item
                break

        if lv2_path is None:
            print(f"⏭️ 跳过 '{lv1_path.name}'：无符合 'XX0...' 规则的子目录")
            continue

        lv1_name = lv1_path.name
        lv2_name = lv2_path.name
        new_top = root / lv2_name

        if new_top.exists():
            print(f"⚠️ 跳过 '{lv1_name}'：目标目录 '{lv2_name}' 已存在")
            continue

        try:
            # 第一步：把二级目录重命名为一级目录的名字
            os.rename(str(lv2_path), str(lv1_path / lv1_name))

            # 第二步：把一级目录重命名为二级目录的名字
            os.rename(str(lv1_path), str(new_top))

            print(f"✅ 成功交换: '{lv1_name}' <-> '{lv2_name}'")

        except OSError as e:
            print(f"💥 失败 '{lv1_name}': {e}")

def main():
    path = input("请输入根目录路径（如 D:\\myfile）：").strip()
    if path:
        swap_folders_by_pattern(path)
    else:
        print("输入不能为空")

if __name__ == "__main__":
    main()
