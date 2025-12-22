import os
import shutil
from pathlib import Path

# ================== 设置区 ==================
# 修改这里为你实际的根目录路径
ROOT = Path(r"K:\hentai\ASMR\41-50")

# 是否在移动后删除已经变空的第一层文件夹（比如 uu 里面没东西了）
DELETE_EMPTY_FIRST_LEVEL = False  # 改成 True 就会自动删除空的父文件夹
# ===========================================

def main():
    if not ROOT.exists():
        print(f"错误：根目录不存在 → {ROOT}")
        return

    print(f"开始处理根目录：{ROOT}")
    print("=" * 50)

    moved_count = 0

    # 遍历第一层子文件夹
    for first_level in ROOT.iterdir():
        if not first_level.is_dir():
            continue  # 跳过文件，只处理文件夹

        print(f"正在处理：{first_level.name}")

        # 遍历这个第一层文件夹里的所有子文件夹（第二层）
        for second_level in list(first_level.iterdir()):  # 用 list 复制避免移动时迭代出错
            if not second_level.is_dir():
                continue  # 只移动文件夹，不动文件

            target_path = ROOT / second_level.name

            if target_path.exists():
                print(f"  [跳过] 根目录已存在同名文件夹：{second_level.name}")
            else:
                try:
                    shutil.move(str(second_level), str(ROOT))
                    print(f"  [成功] 已移动：{second_level.name}")
                    moved_count += 1
                except Exception as e:
                    print(f"  [失败] 移动 {second_level.name} 时出错：{e}")

    # 可选：删除已经变空的第一层文件夹
    if DELETE_EMPTY_FIRST_LEVEL:
        print("\n正在清理空的第一层文件夹...")
        for first_level in ROOT.iterdir():
            if first_level.is_dir() and not any(first_level.iterdir()):
                try:
                    first_level.rmdir()
                    print(f"  已删除空文件夹：{first_level.name}")
                except Exception as e:
                    print(f"  删除 {first_level.name} 失败：{e}")

    print("=" * 50)
    print(f"全部完成！共移动了 {moved_count} 个文件夹。")
    input("\n按回车键退出...")  # 暂停一下，方便看结果


if __name__ == "__main__":
    main()