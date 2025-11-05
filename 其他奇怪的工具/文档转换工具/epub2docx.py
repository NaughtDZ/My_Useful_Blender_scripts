import os
import sys
from pathlib import Path
import pypandoc
import shutil

def clear_console():
    """清空控制台"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """打印横幅"""
    banner = """
    ====================================
          EPUB 转 Word 转换器
    ====================================
    使用方法：
    1. 直接将EPUB文件拖拽到本窗口
    2. 按回车键开始转换
    3. 转换后的文件将保存在原文件同目录下
    
    支持格式：.epub -> .docx
    ====================================
    """
    print(banner)

def check_pandoc_available():
    """检查pandoc是否可用"""
    try:
        pypandoc.get_pandoc_version()
        return True
    except OSError:
        return False

def install_pandoc_windows():
    """在Windows上尝试安装pandoc"""
    print("检测到未安装pandoc，正在尝试自动安装...")
    try:
        import requests
        import tempfile
        import subprocess
        
        # 下载pandoc
        pandoc_url = "https://github.com/jgm/pandoc/releases/download/3.1.9/pandoc-3.1.9-windows-x86_64.msi"
        temp_dir = tempfile.gettempdir()
        msi_path = os.path.join(temp_dir, "pandoc_installer.msi")
        
        print("下载pandoc安装包...")
        response = requests.get(pandoc_url, stream=True)
        with open(msi_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("安装pandoc...")
        result = subprocess.run(['msiexec', '/i', msi_path, '/quiet', '/norestart'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("pandoc安装成功！")
            os.remove(msi_path)
            return True
        else:
            print("pandoc安装失败，请手动安装：https://pandoc.org/installing.html")
            return False
            
    except Exception as e:
        print(f"自动安装失败: {e}")
        print("请手动安装pandoc：https://pandoc.org/installing.html")
        return False

def convert_epub_to_word(epub_path):
    """将EPUB文件转换为Word文档"""
    try:
        epub_path = Path(epub_path)
        
        if not epub_path.exists():
            return False, "文件不存在"
        
        if epub_path.suffix.lower() != '.epub':
            return False, "文件不是EPUB格式"
        
        # 生成输出文件名
        output_path = epub_path.with_suffix('.docx')
        
        # 如果输出文件已存在，添加数字后缀
        counter = 1
        original_output_path = output_path
        while output_path.exists():
            output_path = original_output_path.with_stem(
                f"{original_output_path.stem}_{counter}"
            )
            counter += 1
        
        print(f"正在转换: {epub_path.name}")
        print(f"输出到: {output_path.name}")
        
        # 执行转换
        pypandoc.convert_file(
            str(epub_path),
            'docx',
            outputfile=str(output_path)
        )
        
        return True, f"转换成功！文件已保存为: {output_path.name}"
        
    except Exception as e:
        return False, f"转换失败: {str(e)}"

def get_file_from_drag_drop():
    """通过拖拽获取文件路径"""
    while True:
        print("\n请将EPUB文件拖拽到此处，然后按回车键：")
        
        try:
            # 读取用户输入（拖拽文件会自动填入路径）
            user_input = input().strip()
            
            # 处理拖拽路径（可能包含引号）
            file_path = user_input.strip('"').strip("'")
            
            if not file_path:
                print("未检测到文件路径，请重试。")
                continue
                
            if file_path.lower() == 'exit':
                return None
                
            return file_path
            
        except KeyboardInterrupt:
            print("\n\n用户中断操作，程序退出。")
            sys.exit(0)
        except Exception as e:
            print(f"读取输入时出错: {e}")
            continue

def main():
    """主函数"""
    clear_console()
    print_banner()
    
    # 检查pandoc是否可用
    if not check_pandoc_available():
        print("警告: 未检测到pandoc，转换功能将无法使用。")
        if os.name == 'nt':  # Windows系统
            response = input("是否尝试自动安装pandoc？(y/n): ").lower()
            if response == 'y':
                if not install_pandoc_windows():
                    print("请手动安装pandoc后重新运行本程序。")
                    input("按任意键退出...")
                    return
            else:
                print("请手动安装pandoc：https://pandoc.org/installing.html")
                input("按任意键退出...")
                return
        else:
            print("请手动安装pandoc：https://pandoc.org/installing.html")
            input("按任意键退出...")
            return
    
    print("pandoc已就绪，可以开始转换。")
    
    while True:
        try:
            # 获取文件路径
            file_path = get_file_from_drag_drop()
            
            if file_path is None:
                break
                
            # 转换文件
            success, message = convert_epub_to_word(file_path)
            
            print(message)
            
            if success:
                # 显示文件大小信息
                input_path = Path(file_path)
                output_path = input_path.with_suffix('.docx')
                
                if output_path.exists():
                    input_size = input_path.stat().st_size / 1024 / 1024
                    output_size = output_path.stat().st_size / 1024 / 1024
                    print(f"原文件大小: {input_size:.2f} MB")
                    print(f"生成文件大小: {output_size:.2f} MB")
            
            # 询问是否继续转换
            print("\n是否继续转换其他文件？(y/n): ", end='')
            continue_choice = input().lower().strip()
            
            if continue_choice != 'y':
                print("感谢使用！程序退出。")
                break
                
            clear_console()
            print_banner()
            
        except KeyboardInterrupt:
            print("\n\n用户中断操作，程序退出。")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            continue

if __name__ == "__main__":
    # 检查依赖
    try:
        import pypandoc
    except ImportError:
        print("缺少必要依赖，正在安装...")
        os.system("pip install pypandoc")
        import pypandoc
    
    main()
