import sys
import re
import os


# target_labels
target_labels = ['[PlaybackController]', '[BufferController][video]', '[ThroughputModel]','[haohao]', '[MediaPlayer]']
# regular expression pattern
pattern = re.compile(r'"(.*?)"')

def process_logs(filepath, new_folder):
    # 创建新文件名和目标路径
    filename = os.path.basename(filepath)
    new_filename = f"{filename.split('.')[0]}_filtered.txt"
    new_filepath = os.path.join(new_folder, new_filename)
    
    with open(filepath, 'r') as file, open(new_filepath, 'w') as new_file:
        manual_found = False  # 标记是否找到第一个包含 "Load video" 的行
        for line in file:
            if "Load video" in line and not manual_found:
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

    print(f"筛选结果已写入文件 {new_filepath}")

# main
if len(sys.argv) != 2:
    print("please input the logs dir path.")
    sys.exit(1)

logs_dir = sys.argv[1]

for dirpath, dirnames, filenames in os.walk(logs_dir):
    if dirpath == logs_dir:
        continue

    print(f"current process dir: {dirpath}")
    dir_basename = os.path.basename(dirpath)
    filtered_dirpath = os.path.join(logs_dir, dir_basename + "_filtered")
    print(f"target filtered dir: {filtered_dirpath}")
    if not os.path.exists(filtered_dirpath):
        os.makedirs(filtered_dirpath)
    
    for filename in filenames:
        if filename.endswith(".txt"):
            filepath = os.path.join(dirpath, filename)
            print(f"current process file: {filepath}")
            process_logs(filepath, filtered_dirpath)
