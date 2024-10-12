# haohao: 原始的生成比特率文件的代码，弃用

import sys
import re
import os

# 确保命令行参数正确
if len(sys.argv) != 2:
    print("请提供正确的文件名作为命令行参数！")
    sys.exit(1)

# 获取文件名
filepath = sys.argv[1]
filename = os.path.basename(filepath)

# 创建新文件名和目标标签列表
new_folder_name = "biterates"

pattern = r'_\d{8}-\d{4}_(.*?)_filtered'
match = re.search(pattern, filename)
# pattern = r"log_(.*?)_filtered\.txt$"  
# match = re.search(pattern, filename)  
result = match.group(1)
new_filename = f"{result}_biterates.txt"

new_filepath = os.path.join(new_folder_name, new_filename)
# # 打开原始文件和新文件
try:
    # 创建文件夹
    if not os.path.exists(new_folder_name):
        os.makedirs(new_folder_name)

    # example: [haohao] video bitrate: 97, current time: 6.834648
    # 匹配每行寻找 video bitrate，如果存在，则提取video bitrate的值和时间

    pattern = re.compile(r'video bitrate: (\d+), current time: (\d+\.\d+)')
    with open(filepath, 'r') as file, open(new_filepath, 'w') as new_file:
        for line in file:
            match = pattern.search(line)
            if match:
                bitrate = match.group(1)
                time = match.group(2)
                new_file.write(bitrate + ' ' + time + '\n')
    

    print(f"比特率特征结果已写入文件 {new_filepath}")

except FileNotFoundError:
    print(f"文件 '{filename}' 不存在！")
    sys.exit(1)
