#!/usr/bin/env python3
"""
视频帧率调整与分段工具 - GUI版本
功能：
1. 检查并调整视频帧率到目标帧率（不丢帧）
2. 按帧数或时间分段输出视频
3. 保持原始编码参数，尽可能无损
4. 纯Python GUI，无需第三方库
"""

import os
import sys
import subprocess
import json
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import re

class VideoProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("视频帧率调整与分段工具")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # 变量
        self.input_file = tk.StringVar()
        self.target_fps = tk.StringVar(value="24")
        self.segment_mode = tk.StringVar(value="frames")  # frames 或 time
        self.segment_frames = tk.StringVar(value="120")
        self.segment_time = tk.StringVar(value="5")
        self.output_dir = tk.StringVar()
        self.is_processing = False
        
        self.setup_ui()
        self.check_ffmpeg()
    
    def setup_ui(self):
        """创建UI界面"""
        # 主容器
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title_label = ttk.Label(main_frame, text="视频帧率调整与分段工具", 
                                font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="输入文件", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(file_frame, text="视频文件:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(file_frame, textvariable=self.input_file, width=50).grid(row=0, column=1, padx=(5, 5))
        ttk.Button(file_frame, text="浏览", command=self.select_file).grid(row=0, column=2)
        
        # 视频信息显示
        self.info_label = ttk.Label(file_frame, text="未选择文件", foreground="gray")
        self.info_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))
        
        # 帧率设置区域
        fps_frame = ttk.LabelFrame(main_frame, text="帧率设置", padding="10")
        fps_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(fps_frame, text="目标帧率 (FPS):").grid(row=0, column=0, sticky=tk.W)
        fps_entry = ttk.Entry(fps_frame, textvariable=self.target_fps, width=10)
        fps_entry.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        ttk.Label(fps_frame, text="(例如: 24, 30, 60)").grid(row=0, column=2, sticky=tk.W, padx=(5, 0))
        
        # 分段设置区域
        segment_frame = ttk.LabelFrame(main_frame, text="分段设置", padding="10")
        segment_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 分段模式选择
        mode_frame = ttk.Frame(segment_frame)
        mode_frame.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(mode_frame, text="分段模式:").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(mode_frame, text="按帧数", variable=self.segment_mode, 
                       value="frames", command=self.update_segment_inputs).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(mode_frame, text="按时间(秒)", variable=self.segment_mode, 
                       value="time", command=self.update_segment_inputs).pack(side=tk.LEFT)
        
        # 分段参数输入
        self.segment_input_frame = ttk.Frame(segment_frame)
        self.segment_input_frame.grid(row=1, column=0, columnspan=3, sticky=tk.W)
        
        self.segment_label = ttk.Label(self.segment_input_frame, text="每段帧数:")
        self.segment_label.pack(side=tk.LEFT)
        
        self.segment_entry = ttk.Entry(self.segment_input_frame, textvariable=self.segment_frames, width=10)
        self.segment_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        self.segment_unit_label = ttk.Label(self.segment_input_frame, text="帧 (约5秒@24fps)")
        self.segment_unit_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 输出目录
        dir_frame = ttk.LabelFrame(main_frame, text="输出设置", padding="10")
        dir_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(dir_frame, text="输出目录:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(dir_frame, textvariable=self.output_dir, width=40).grid(row=0, column=1, padx=(5, 5))
        ttk.Button(dir_frame, text="浏览", command=self.select_output_dir).grid(row=0, column=2)
        
        # 进度条和按钮
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.progress = ttk.Progressbar(control_frame, mode='indeterminate', length=300)
        self.progress.pack(side=tk.LEFT, padx=(0, 10))
        
        self.process_btn = ttk.Button(control_frame, text="开始处理", command=self.start_processing)
        self.process_btn.pack(side=tk.LEFT)
        
        ttk.Button(control_frame, text="停止", command=self.stop_processing).pack(side=tk.LEFT, padx=(5, 0))
        
        # 日志区域
        log_frame = ttk.LabelFrame(main_frame, text="处理日志", padding="10")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame, height=12, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text['yscrollcommand'] = scrollbar.set
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        file_frame.columnconfigure(1, weight=1)
        dir_frame.columnconfigure(1, weight=1)
        
        # 初始状态
        self.update_segment_inputs()
    
    def update_segment_inputs(self):
        """更新分段输入框的标签"""
        if self.segment_mode.get() == "frames":
            self.segment_label.config(text="每段帧数:")
            self.segment_unit_label.config(text="帧 (约5秒@24fps)")
            self.segment_entry.config(textvariable=self.segment_frames)
        else:
            self.segment_label.config(text="每段时间(秒):")
            self.segment_unit_label.config(text="秒")
            self.segment_entry.config(textvariable=self.segment_time)
    
    def check_ffmpeg(self):
        """检查ffmpeg是否可用"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            subprocess.run(['ffprobe', '-version'], capture_output=True, check=True)
            self.log("✓ FFmpeg和FFprobe已找到")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.log("✗ 错误: 找不到FFmpeg。请确保ffmpeg和ffprobe在PATH中")
            messagebox.showerror("错误", "找不到FFmpeg！\n请确保ffmpeg和ffprobe已安装并在系统PATH中。")
    
    def select_file(self):
        """选择输入文件"""
        filetypes = [
            ("视频文件", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.m4v"),
            ("所有文件", "*.*")
        ]
        filename = filedialog.askopenfilename(title="选择视频文件", filetypes=filetypes)
        if filename:
            self.input_file.set(filename)
            self.show_video_info(filename)
            # 自动设置输出目录
            if not self.output_dir.get():
                self.output_dir.set(os.path.dirname(filename))
    
    def show_video_info(self, filepath):
        """显示视频信息"""
        try:
            info = self.get_video_info(filepath)
            self.info_label.config(
                text=f"帧率: {info['fps']:.2f} FPS | 总帧数: {info['nb_frames']} | "
                     f"时长: {info['duration']:.2f}s | 编码: {info['codec']} | "
                     f"分辨率: {info['width']}x{info['height']}",
                foreground="black"
            )
            self.log(f"视频信息: {info['fps']:.2f}FPS, {info['nb_frames']}帧, "
                    f"{info['duration']:.2f}秒")
        except Exception as e:
            self.log(f"读取视频信息失败: {e}")
    
    def get_video_info(self, input_path):
        """使用ffprobe获取视频信息"""
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_streams',
            '-show_format',
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        video_stream = None
        for stream in data['streams']:
            if stream['codec_type'] == 'video':
                video_stream = stream
                break
        
        if not video_stream:
            raise ValueError("未找到视频流")
        
        fps_str = video_stream.get('r_frame_rate', '0/0')
        if '/' in fps_str:
            num, den = fps_str.split('/')
            fps = float(num) / float(den) if float(den) != 0 else 0
        else:
            fps = float(fps_str)
        
        nb_frames = video_stream.get('nb_frames')
        if nb_frames is None:
            duration = float(data['format']['duration'])
            nb_frames = int(duration * fps)
        
        return {
            'fps': fps,
            'nb_frames': int(nb_frames),
            'duration': float(data['format']['duration']),
            'codec': video_stream.get('codec_name', 'h264'),
            'width': int(video_stream.get('width', 0)),
            'height': int(video_stream.get('height', 0))
        }
    
    def select_output_dir(self):
        """选择输出目录"""
        dirname = filedialog.askdirectory(title="选择输出目录")
        if dirname:
            self.output_dir.set(dirname)
    
    def log(self, message):
        """添加日志"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_processing(self):
        """开始处理"""
        if self.is_processing:
            return
        
        # 验证输入
        if not self.input_file.get():
            messagebox.showerror("错误", "请选择输入视频文件")
            return
        
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("错误", "输入文件不存在")
            return
        
        try:
            target_fps = float(self.target_fps.get())
            if target_fps <= 0:
                raise ValueError("帧率必须大于0")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的目标帧率")
            return
        
        if self.segment_mode.get() == "frames":
            try:
                frames = int(self.segment_frames.get())
                if frames <= 0:
                    raise ValueError("帧数必须大于0")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的帧数")
                return
        else:
            try:
                time_sec = float(self.segment_time.get())
                if time_sec <= 0:
                    raise ValueError("时间必须大于0")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的时间(秒)")
                return
        
        # 开始处理
        self.is_processing = True
        self.process_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.log_text.delete(1.0, tk.END)
        self.log("开始处理视频...")
        
        # 在新线程中处理
        thread = threading.Thread(target=self.process_video, daemon=True)
        thread.start()
    
    def stop_processing(self):
        """停止处理"""
        if self.is_processing:
            self.is_processing = False
            self.log("正在停止处理...")
    
    def process_video(self):
        """处理视频的主函数"""
        try:
            input_path = self.input_file.get()
            target_fps = float(self.target_fps.get())
            output_dir = self.output_dir.get()
            
            if not output_dir:
                output_dir = os.path.dirname(input_path)
            
            # 获取视频信息
            self.log("正在分析视频...")
            info = self.get_video_info(input_path)
            self.log(f"原始: {info['fps']:.2f}FPS, {info['nb_frames']}帧, {info['duration']:.2f}秒")
            
            # 准备输出文件名
            base_name = Path(input_path).stem
            ext = Path(input_path).suffix
            
            # 调整帧率
            if abs(info['fps'] - target_fps) > 0.01:
                self.log(f"调整帧率: {info['fps']:.2f} -> {target_fps}FPS")
                temp_file = f"{base_name}_{target_fps}fps{ext}"
                adjusted_path = self.adjust_fps(input_path, temp_file, info['fps'], target_fps)
                if not self.is_processing:
                    self.log("处理被用户取消")
                    return
                # 重新获取信息
                info = self.get_video_info(adjusted_path)
                self.log(f"调整后: {info['fps']:.2f}FPS, {info['nb_frames']}帧")
            else:
                adjusted_path = input_path
                self.log("视频已是目标帧率，跳过调整")
            
            # 分段
            self.log("开始分段...")
            segment_frames = None
            segment_time = None
            
            if self.segment_mode.get() == "frames":
                segment_frames = int(self.segment_frames.get())
                self.log(f"按帧数分段: {segment_frames}帧/段")
            else:
                segment_time = float(self.segment_time.get())
                self.log(f"按时间分段: {segment_time}秒/段")
            
            self.split_video(adjusted_path, output_dir, f"{base_name}{ext}", 
                           segment_frames, segment_time)
            
            # 清理临时文件
            if adjusted_path != input_path and os.path.exists(adjusted_path):
                os.remove(adjusted_path)
                self.log(f"清理临时文件: {adjusted_path}")
            
            self.log(f"\n✓ 处理完成! 文件保存在: {output_dir}/")
            messagebox.showinfo("完成", f"视频处理完成！\n输出目录: {output_dir}")
            
        except Exception as e:
            self.log(f"✗ 错误: {str(e)}")
            messagebox.showerror("错误", f"处理失败: {str(e)}")
        finally:
            self.is_processing = False
            self.process_btn.config(state=tk.NORMAL)
            self.progress.stop()
    
    def adjust_fps(self, input_path, output_path, current_fps, target_fps):
        """调整视频帧率"""
        speed_ratio = current_fps / target_fps
        audio_speed = 1 / speed_ratio
        
        self.log(f"变速比: {speed_ratio:.4f}, 音频变速: {audio_speed:.4f}")
        
        # 处理音频变速超出范围的情况
        if audio_speed < 0.5 or audio_speed > 2.0:
            self.log("音频变速超出范围，使用多步变速")
            # 简化的多步变速处理
            import math
            target = audio_speed
            speeds = []
            
            if target < 0.5:
                while target < 0.5:
                    speeds.append(0.5)
                    target /= 0.5
                speeds.append(target)
            elif target > 2.0:
                while target > 2.0:
                    speeds.append(2.0)
                    target /= 2.0
                speeds.append(target)
            else:
                speeds = [target]
            
            atempo_filters = [f"atempo={s:.6f}" for s in speeds]
            atempo_chain = ",".join(atempo_filters)
            filter_complex = f'[0:v]setpts=PTS*{speed_ratio:.6f}[v];[0:a]{atempo_chain}[a]'
        else:
            filter_complex = f'[0:v]setpts=PTS*{speed_ratio:.6f}[v];[0:a]atempo={audio_speed:.6f}[a]'
        
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-filter_complex', filter_complex,
            '-map', '[v]',
            '-map', '[a]',
            '-c:v', 'libx264',
            '-crf', '19',
            '-preset', 'medium',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-fps_mode', 'vfr',
            '-y',
            output_path
        ]
        
        self.log(f"执行FFmpeg命令...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            self.log("FFmpeg错误输出:")
            self.log(result.stderr)
            raise subprocess.CalledProcessError(result.returncode, cmd)
        
        return output_path
    
    def split_video(self, input_path, output_dir, filename, segment_frames=None, segment_time=None):
        """分段视频"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        output_pattern = os.path.join(output_dir, f"%05d_{filename}")
        
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-c', 'copy',
            '-map', '0',
            '-f', 'segment',
            '-reset_timestamps', '1',
            '-avoid_negative_ts', 'make_zero'
        ]
        
        if segment_frames:
            # 按帧数分段：需要先计算时间
            info = self.get_video_info(input_path)
            segment_duration = segment_frames / info['fps']
            cmd.extend(['-segment_time', str(segment_duration)])
            self.log(f"每段时长: {segment_duration:.2f}秒")
        else:
            cmd.extend(['-segment_time', str(segment_time)])
        
        cmd.append(output_pattern)
        
        self.log(f"执行分段命令...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            self.log("FFmpeg错误输出:")
            self.log(result.stderr)
            raise subprocess.CalledProcessError(result.returncode, cmd)

def main():
    root = tk.Tk()
    app = VideoProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()