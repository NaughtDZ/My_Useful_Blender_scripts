import os
from pathlib import Path

def swap_rj_by_rename(root_dir_str):
    root = Path(root_dir_str).resolve()
    if not root.is_dir():
        print(f"❌ 根目录无效: {root}")
        return

    for lv1_path in root.iterdir():
        if not lv1_path.is_dir():
            continue

        # 找第一个以 'RJ' 开头的子目录
        lv2_path = None
        for item in lv1_path.iterdir():
            if item.is_dir() and item.name.startswith('RJ'):
                lv2_path = item
                break

        if lv2_path is None:
            print(f"⏭️ 跳过 '{lv1_path.name}'：无 RJ 开头子目录")
            continue

        lv1_name = lv1_path.name      # 比如 "letsgo"
        lv2_name = lv2_path.name      # 比如 "RJ12345-Giok"
        new_top = root / lv2_name     # 最终的一级目录路径

        if new_top.exists():
            print(f"⚠️ 跳过 '{lv1_name}'：'{lv2_name}' 已存在")
            continue

        try:
            # 第一步：把二级目录 RJ12345 重命名为 lv1 的名字（比如 letsgo）
            os.rename(str(lv2_path), str(lv1_path / lv1_name))

            # 第二步：把一级目录 letsgo 重命名为 RJ12345
            os.rename(str(lv1_path), str(new_top))

            print(f"✅ 成功交换: '{lv1_name}' <-> '{lv2_name}'")

        except OSError as e:
            print(f"💥 失败 '{lv1_name}': {e}")

def main():
    path = input("请输入根目录路径（如 D:\\myfile）：").strip()
    if path:
        swap_rj_by_rename(path)
    else:
        print("输入不能为空")

if __name__ == "__main__":
    main()