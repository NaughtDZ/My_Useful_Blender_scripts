# move_wide_images_interactive.py

import os
import shutil
from pathlib import Path
from PIL import Image

def is_wide_enough(image_path, min_ratio):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            if width <= height:  # 纵图或正方形直接排除
                return False
            return width / height >= min_ratio
    except Exception:
        return False


def main():
    print("=" * 60)
    print("   横向宽图（≥4:3）自动搬家工具   ".center(60, " "))
    print("=" * 60)
    print()

    # 1. 源目录
    while True:
        source = input("请输入要扫描的图片文件夹路径（直接拖文件夹到这里回车即可）:\n").strip('"\' ')
        source_path = Path(source)
        if source_path.exists() and source_path.is_dir():
            break
        print("【错误】这个路径不存在或不是文件夹，请重新输入！\n")

    # 2. 目标目录
    while True:
        default_target = source_path.parent / (source_path.name + "_宽图4比3及以上")
        print(f"\n建议保存到：{default_target}")
        target_input = input("请输入目标文件夹路径（直接回车使用上面建议的路径）:\n").strip('"\' ')
        if not target_input:
            target_path = default_target
        else:
            target_path = Path(target_input)
        target_path.mkdir(parents=True, exist_ok=True)
        if target_path.is_dir():
            break
        print("【错误】目标路径无法创建，请换一个！\n")

    # 3. 宽高比阈值
    print("\n常见宽高比参考：")
    print("   4:3  → 1.333  (普通老照片、平板)")
    print("   16:9 → 1.778  (宽屏显示器、视频)")
    print("   21:9 → 2.333  (超宽屏)")
    while True:
        ratio_input = input(f"\n请输入最小宽高比（回车默认 4:3 ≈ 1.333）:\n").strip()
        if not ratio_input:
            min_ratio = 4/3
            break
        try:
            min_ratio = float(ratio_input)
            if min_ratio <= 1:
                print("宽高比必须大于1（否则就不是横图了）")
                continue
            break
        except:
            print("请输入正确的数字！")

    # 4. 移动还是复制
    print("\n操作方式：")
    print("1. 移动（原图会消失，推荐，省空间）")
    print("2. 复制（原图保留，安全）")
    while True:
        choice = input("请选择 1 或 2（回车默认 1 移动）:\n").strip()
        if choice in ["", "1"]:
            copy_mode = False
            action_text = "移动"
            break
        elif choice == "2":
            copy_mode = True
            action_text = "复制"
            break
        print("只能输入 1 或 2 哦~")

    # 5. 是否递归子文件夹
    print("\n是否扫描子文件夹？")
    print("1. 只扫描当前文件夹")
    print("2. 递归扫描所有子文件夹（推荐，大部分人选这个）")
    while True:
        rec_choice = input("请选择 1 或 2（回车默认 2 递归）:\n").strip()
        if rec_choice in ["", "2"]:
            recursive = True
            break
        elif rec_choice == "1":
            recursive = False
            break

    print("\n" + "=" * 60)
    print("开始干活啦！参数如下：")
    print(f"源文件夹     → {source_path}")
    print(f"目标文件夹   → {target_path}")
    print(f"宽高比阈值   → ≥ {min_ratio:.3f}（约 {min_ratio*3:.2f}:3）")
    print(f"操作方式     → {action_text}")
    print(f"扫描模式     → {'递归所有子文件夹' if recursive else '只当前文件夹'}")
    print("=" * 60)
    input("\n按回车键开始处理...（想反悔就关掉窗口）\n")

    # 开始处理
    extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff', '.tif', '.heic', '.heif'}
    iterator = source_path.rglob("*") if recursive else source_path.iterdir()

    moved = 0
    skipped = 0

    for file_path in iterator:
        if file_path.is_file() and file_path.suffix.lower() in extensions:
            if is_wide_enough(file_path, min_ratio):
                dest = target_path / file_path.name

                # 重名处理
                stem = dest.stem
                suffix = dest.suffix
                counter = 1
                while dest.exists():
                    dest = target_path / f"{stem}_{counter}{suffix}"
                    counter += 1

                try:
                    if copy_mode:
                        shutil.copy2(file_path, dest)
                    else:
                        shutil.move(str(file_path), dest)
                    print(f"✓ {action_text}: {file_path.name}")
                    moved += 1
                except Exception as e:
                    print(f"✗ 失败 {file_path.name}: {e}")
            else:
                skipped += 1

    print("\n" + "完成！".center(50, "="))
    print(f"共 {action_text} {moved} 张宽图到：")
    print(f"{target_path}")
    print(f"（跳过了 {skipped} 张不符合条件的图片）")
    print("\n3秒后自动关闭窗口，或者你现在可以关掉了~")
    import time
    time.sleep(3)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户取消了操作，再见！")
    except Exception as e:
        print(f"\n程序出错了：{e}")
        input("按回车退出...")
