import os
import subprocess
import argparse
import sys

def get_total_frames(video_path):
    """使用 ffprobe 获取视频总帧数"""
    cmd = [
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-count_packets', '-show_entries', 'stream=nb_read_packets',
        '-of', 'csv=p=0', video_path
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return int(result.stdout.strip())
    except Exception as e:
        print(f"获取帧数失败: {e}")
        return None

def extract_frames(video_path, output_dir, img_format='png'):
    """每隔5帧（包括第1帧）提取帧"""
    os.makedirs(output_dir, exist_ok=True)

    total_frames = get_total_frames(video_path)
    if total_frames is None:
        print("无法获取视频帧数，尝试直接使用过滤器...")
        total_frames = "未知"

    print(f"视频总帧数: {total_frames}")
    print(f"开始提取每隔5帧的图像（含第1帧） → {output_dir}")

    # -vf "select='not(mod(n,5))'" 表示：帧号 n 除以5余数不为0的跳过 → 保留 1,6,11,16...
    # 实际上 not(mod(n,5)) 就是 mod(n,5)==0 → 0,5,10,15... 这是第1、6、11...帧（从0开始计数）
    # 但你想要的是第1、6、11...（即每5帧一次，包含第1帧）
    # 正确写法：select='eq(mod(n,5),0)' 或者更直观：
    # 由于 ffmpeg 帧从 0 开始：第1帧是 n=0, 第6帧是 n=5
    # 所以：select='not(mod(n\,5))' 实际上是错的！应为：
    # 正确：select='mod(n,5)==0'  → n=0,5,10,15... 即第1、6、11...帧

    filter_expr = "select='mod(n,5)==0',setpts=N/FRAME_RATE/TB"

    output_pattern = os.path.join(output_dir, "frame_%08d." + img_format)

    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vf', filter_expr,
        '-vsync', '0',           # 避免重复帧
        '-frame_pts', '1',       # 输出文件名使用真实 pts
        output_pattern,
        '-y'                     # 覆盖已有文件
    ]

    print(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("提取失败！")
        print(result.stderr)
        return False
    else:
        print("提取完成！")
        return True

def main():
    parser = argparse.ArgumentParser(description="每隔5帧（含第1帧）提取视频帧")
    parser.add_argument("video", help="输入视频文件路径")
    parser.add_argument("-o", "--output", default="frames_output", help="输出文件夹 (默认: frames_output)")
    parser.add_argument("-f", "--format", default="png", choices=['png', 'jpg'], help="图片格式: png 或 jpg (默认: png)")

    args = parser.parse_args()

    if not os.path.isfile(args.video):
        print(f"错误：视频文件不存在 → {args.video}")
        sys.exit(1)

    extract_frames(args.video, args.output, args.format)

if __name__ == "__main__":
    main()
