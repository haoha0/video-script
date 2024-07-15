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
new_folder_name = "filtered_logs"
new_filename = f"{filename.split('.')[0]}_filtered.txt"
new_filepath = os.path.join(new_folder_name, new_filename)
# target_labels = ['[PlaybackController]', '[video]', '[haohao]', '[MediaPlayer]']    # TODO
target_labels = ['[PlaybackController]', '[BufferController][video]', '[ThroughputModel]','[haohao]', '[MediaPlayer]']

# 编译正则表达式，用于匹配第一个双引号及其后的内容
pattern = re.compile(r'"(.*?)"')

# 打开原始文件和新文件
try:
    # 创建文件夹
    if not os.path.exists(new_folder_name):
        os.makedirs(new_folder_name)
    
    with open(filepath, 'r') as file, open(new_filepath, 'w') as new_file:
        manual_found = False  # 标记是否找到第一个包含 "Manual" 的行
        for line in file:
            if "Manual" in line and not manual_found:
            # if "Auto" in line and not manual_found:
                manual_found = True
            
            if manual_found:
                # 判断行中是否含有目标标签
                if any(label in line for label in target_labels):
                    # 使用正则表达式进行匹配
                    match = pattern.search(line)
                    if match:
                        content = match.group(1)
                        new_file.write(content + '\n')
except FileNotFoundError:
    print(f"文件 '{filename}' 不存在！")
    sys.exit(1)

print(f"筛选结果已写入文件 {new_filepath}")
