import os
import subprocess
import sys

def run_ffmpeg_command(command):
    """运行FFmpeg命令并处理错误"""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg执行失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    except FileNotFoundError:
        print("错误: 找不到ffmpeg。请确保ffmpeg已添加到环境变量中。")
        return False

def get_file_path(prompt):
    """获取用户拖放的文件路径"""
    while True:
        file_path = input(prompt).strip().strip('"')
        if os.path.exists(file_path):
            return file_path
        else:
            print("文件不存在，请重新拖放文件:")

def main():
    print("=== 视频音频处理脚本 ===\n")
    
    # 步骤1: 获取输出文件名
    filename = input("请输入输出视频文件的名称（不含扩展名）: ").strip()
    if not filename:
        print("文件名不能为空!")
        return
    
    output_video = f"{filename}.mp4"
    
    # 检查输出文件是否已存在
    if os.path.exists(output_video):
        overwrite = input(f"文件 {output_video} 已存在，是否覆盖? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("操作已取消。")
            return
    
    # 步骤2: 处理有音频的视频文件
    print("\n步骤1: 请拖放一个有音频轨的视频文件")
    video_with_audio = get_file_path("拖放文件: ")
    
    audio_output = f"{filename}_audio.m4a"
    
    print("正在提取音频...")
    ffmpeg_cmd1 = [
        "ffmpeg", "-i", video_with_audio,
        "-vn", "-c:a", "copy", audio_output,
        "-y"  # 覆盖已存在的文件
    ]
    
    if not run_ffmpeg_command(ffmpeg_cmd1):
        print("音频提取失败!")
        return
    
    print(f"音频已保存为: {audio_output}")
    
    # 步骤3: 处理无音频的视频文件并合并
    print("\n步骤2: 请拖放一个没有音频轨的视频文件")
    video_without_audio = get_file_path("拖放文件: ")
    
    print("正在合并视频和音频...")
    ffmpeg_cmd2 = [
        "ffmpeg", "-i", video_without_audio, "-i", audio_output,
        "-c:v", "copy", "-c:a", "copy", output_video,
        "-y"  # 覆盖已存在的文件
    ]
    
    if run_ffmpeg_command(ffmpeg_cmd2):
        print(f"\n处理完成! 最终视频已保存为: {output_video}")
        
        # 询问是否删除临时音频文件
        delete_audio = input(f"是否删除临时音频文件 {audio_output}? (y/n): ").strip().lower()
        if delete_audio == 'y':
            try:
                os.remove(audio_output)
                print("临时文件已删除。")
            except OSError as e:
                print(f"删除临时文件失败: {e}")
    else:
        print("视频合并失败!")

if __name__ == "__main__":
    main()