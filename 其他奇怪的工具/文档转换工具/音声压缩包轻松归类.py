# -*- coding: utf-8 -*-
# 文件名: split_rar_video_priority.py
# 视频优先，一次性搬家，不复制


import os
import rarfile
import shutil
from pathlib import Path

# 常见视频后缀（缺的自己加就行）
VIDEO_EXT = {'.mp4', '.avi', '.mkv', '.wmv', '.mov', '.flv', '.webm', 
             '.mpg', '.mpeg', '.m4v', '.ts', '.m2ts', '.rmvb', '.rm', '.ogv', '.3gp'}

scan_dir = Path(".")
#Unrar.exe路径
rarfile.UNRAR_TOOL = "C:/Program Files/WinRAR/UnRAR.exe"

has_video_dir = scan_dir / "01_有视频_优先"
has_wav_only_dir = scan_dir / "02_纯WAV无视频"

has_video_dir.mkdir(exist_ok=True)
has_wav_only_dir.mkdir(exist_ok=True)

for rar_path in scan_dir.glob("*.rar"):
    if not rar_path.is_file():
        continue
        
    has_wav = False
    has_video = False
    
    try:
        with rarfile.RarFile(rar_path) as rf:
            for entry in rf.infolist():
                if entry.isdir():
                    continue
                name_low = entry.filename.lower()
                if name_low.endswith('.wav'):
                    has_wav = True
                if any(name_low.endswith(ext) for ext in VIDEO_EXT):
                    has_video = True
                    break                      # 发现视频立刻跳出，加速
                if has_video and has_wav:       # 其实这里已经不需要了
                    break
    except rarfile.BadRarFile:
        print(f"【损坏/有密码】{rar_path.name}")
        continue
    except Exception as e:
        print(f"【读取异常】{rar_path.name} → {e}")
        continue
    
    # 严格视频优先
    if has_video:
        shutil.move(str(rar_path), str(has_video_dir / rar_path.name))
        print(f"【有视频】→ {rar_path.name}")
    elif has_wav:
        shutil.move(str(rar_path), str(has_wav_only_dir / rar_path.name))
        print(f"【纯WAV】→ {rar_path.name}")
    else:
        print(f"【无音视频】{rar_path.name}（留在原地）")

print("\n全部搞定！视频优先分类完成～")