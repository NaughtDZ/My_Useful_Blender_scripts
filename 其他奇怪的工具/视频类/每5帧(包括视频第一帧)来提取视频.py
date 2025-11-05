import subprocess
import os
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("请将视频文件拖放到此脚本上")
        print("支持拖放多个视频文件")
        input("按回车键退出...")
        return
    
    video_files = sys.argv[1:]
    
    for video_path in video_files:
        video = Path(video_path)
        if not video.exists():
            print(f"✗ 文件不存在: {video}")
            continue
            
        # 为每个视频创建独立的输出目录
        output_dir = f"{video.stem}_frames"
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # 带视频名前缀的输出格式
        output_pattern = output_path / f"{video.stem}_frame_%05d.png"
        
        # FFmpeg命令
        cmd = [
            'ffmpeg',
            '-i', str(video),
            '-vf', 'select=not(mod(n\,5))',
            '-vsync', 'vfr',
            '-q:v', '2',
            str(output_pattern)
        ]
        
        try:
            print(f"正在处理: {video.name}")
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✓ 完成! 截图保存在: {output_dir}")
        except subprocess.CalledProcessError as e:
            print(f"✗ 处理失败: {video.name}")
        except FileNotFoundError:
            print("✗ 错误: 未找到ffmpeg，请确保已添加到环境变量")
            break
    
    print("\n所有视频处理完成!")
    input("按回车键退出...")

if __name__ == "__main__":
    main()
