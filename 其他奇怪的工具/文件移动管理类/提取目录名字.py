import os

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 获取该目录下的所有条目
entries = os.listdir(script_dir)

# 过滤出只有第一层目录（不是文件）
directories = [entry for entry in entries if os.path.isdir(os.path.join(script_dir, entry))]

# 按名字排序（推荐，这样输出更有序）
directories.sort()

# 用逗号拼接成字符串
output_str = ','.join(directories)

# 输出文件名（放在脚本同目录下）
output_file = os.path.join(script_dir, 'directories.txt')

# 写入文件（使用UTF-8编码，以防目录名有特殊字符）
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(output_str)

print(f"已成功提取 {len(directories)} 个目录，并写入 {output_file}")
print("内容预览：")
print(output_str)