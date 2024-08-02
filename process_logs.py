# haohao: process original logs to get the filtered logs and generate bitrates and resolution index
# Usage: python process_logs.py logs_dir
# logs_dir: the dir path of the original logs
# eg: python3 .\process_logs.py .\0724_ground_logs\
# eg: python3 .\process_logs.py ..\..\pcap_data\0724_ground_logs_test\
# output:
# 1. the filtered logs in the _filtered dir
# 2. the bitrates in the _biterates dir
# 3. the resolution index in the _index dir

import sys
import re
import os


# target_labels
target_labels = ['[PlaybackController]', '[BufferController][video]', '[ThroughputModel]','[haohao]', '[MediaPlayer]']
# regular expression pattern
log_pattern = re.compile(r'"(.*?)"')

# input
# filepath: the path of the original log file
# new_filepath: the path of the new file to store the filtered logs
def process_logs(filepath, new_filepath):
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
                    match = log_pattern.search(line)
                    if match:
                        content = match.group(1)
                        new_file.write(content + '\n')

    print(f"筛选结果已写入文件 {new_filepath}")

def generate_bitrates(filepath, bitrates_filepath, index_filepath):
    # "[haohao] video bitrate: 491, current time: 0.011149"
    # "[haohao] video quality index: 4"
    # bitrate_pattern = re.compile(r'video bitrate: (\d+), current time: (\d+\.\d+)')
    bitrate_pattern = re.compile(r'video bitrate: (\d+), current time: (\d+\.\d+)')
    index_pattern = re.compile(r'video quality index: (\d+)')
    playback_pattern = re.compile(r'playbackPlaying')

    start_matching = False

    with open(filepath, 'r') as file, open(bitrates_filepath, 'w') as new_file, open(index_filepath, 'w') as index_file:
        for line in file:
            if not start_matching:
                if playback_pattern.search(line):
                    start_matching = True
                continue
            
            bitrate_match = bitrate_pattern.search(line)
            index_match = index_pattern.search(line)
            if bitrate_match:
                bitrate = bitrate_match.group(1)
                time = bitrate_match.group(2)
                new_file.write(bitrate + ' ' + time + '\n')
            if index_match:
                index = index_match.group(1)
                index_file.write(index + '\n')

    print(f"比特率特征结果已写入文件 {bitrates_filepath}")
    print(f"分辨率指数结果已写入文件 {index_filepath}")
    print("")
    
    # with open(filepath, 'r') as file, open(new_filepath, 'w') as new_file:
    #     for line in file:
    #         match = pattern.search(line)
    #         if match:
    #             bitrate = match.group(1)
    #             time = match.group(2)
    #             new_file.write(bitrate + ' ' + time + '\n')

    # print(f"比特率特征结果已写入文件 {new_filepath}")

# main
if len(sys.argv) != 2:
    print("please input the logs dir path.")
    sys.exit(1)
logs_dir = sys.argv[1]

for dirpath, dirnames, filenames in os.walk(logs_dir):
    # skip the logs dir, the filtered dir and the bitrates dir
    if dirpath == logs_dir or dirpath.endswith("_filtered") or dirpath.endswith("_bitrates") or dirpath.endswith("_index"):
        continue
    print(f"current process dir: {dirpath}")
    dir_basename = os.path.basename(dirpath)

    # create filtered dir
    filtered_dirpath = os.path.join(logs_dir, dir_basename + "_filtered")
    print(f"target filtered dir: {filtered_dirpath}")
    if not os.path.exists(filtered_dirpath):
        os.makedirs(filtered_dirpath)
    
    # create bitrates dir
    bitrates_dirpath = os.path.join(logs_dir, dir_basename + "_bitrates")
    print(f"target bitrates dir: {bitrates_dirpath}")
    if not os.path.exists(bitrates_dirpath):
        os.makedirs(bitrates_dirpath)

    # create index dir
    index_dirpath = os.path.join(logs_dir, dir_basename + "_index")
    print(f"target index dir: {index_dirpath}")
    if not os.path.exists(index_dirpath):
        os.makedirs(index_dirpath)

    for filename in filenames:
        if filename.endswith(".txt"):
            filepath = os.path.join(dirpath, filename)

            # process
            new_filename = f"{filename.split('.')[0]}_filtered.txt"
            filtered_filepath = os.path.join(filtered_dirpath, new_filename)
            print(f"current process file: {filepath}")

            process_logs(filepath, filtered_filepath)

            # generate bitrates and index
            filtered_filename = os.path.basename(filtered_filepath)
            pattern = r"log_(.*?)_filtered\.txt$"  
            match = re.search(pattern, filtered_filename)  
            result = match.group(1)
            # bitrates
            bitrates_filename = f"{result}_bitrates.txt"
            bitrates_filepath = os.path.join(bitrates_dirpath, bitrates_filename)
            # index
            index_filename = f"{result}_index.txt"
            index_filepath = os.path.join(index_dirpath, index_filename)

            generate_bitrates(filtered_filepath, bitrates_filepath, index_filepath)
