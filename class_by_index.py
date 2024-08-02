# 遍历给定目录下所有以index结尾的文件夹，处理文件夹下面的所有txt文件
# 每个txt文件中为一次视频播放每个时刻的分辨率指数，每一行一个数字

# 为每种分辨率分配一个index指数，即144p为1,240p为2,360p为3,480p为4,720p为5,1080p为6
# 设定三种视频质量等级区间：
# low definition(LD): [1, 3)
# standard definition(SD): [3, 4.5)
# high definition(HD): [4.5, 6]

# 设定视频质量等级对应的三个list，存储每个视频对应文件的base name和平均分辨率指数
# 计算每个视频播放的平均分辨率，划分到对应的区间

# usage: python class_by_index.py logs_dir
# eg: python3 .\class_by_index.py ..\..\pcap_data\0724_ground_logs_test\

import os
import sys

# return: file basename and avg resolution index
def read_index(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    resolution_index = sum(int(line) for line in lines) / len(lines)
    basename = '_'.join(os.path.basename(file_path).split('_')[:-1])

    return basename, resolution_index


def class_resolution_index(logs_dir):
    LD_list = []
    SD_list = []
    HD_list = []

    dirs = os.listdir(logs_dir) # 列出指定目录下的所有文件和目录名，返回的是一个列表
    for dir in dirs:
        if dir.endswith('index'):
            print("processing dir: ", dir)
            dir_path = os.path.join(logs_dir, dir)

            for file in os.listdir(dir_path):
                if file.endswith('txt'):
                    print("processing file: ", file)
                    file_path = os.path.join(dir_path, file)
                    
                    basename, avg_resolution_index = read_index(file_path)
                    print("basename: ", basename, " avg resolution index: ", avg_resolution_index)

                    # 划分到对应的区间
                    if avg_resolution_index >= 1 and avg_resolution_index < 3:
                        LD_list.append((basename, avg_resolution_index))
                    elif avg_resolution_index >= 3 and avg_resolution_index < 4.5:
                        SD_list.append((basename, avg_resolution_index))
                    elif avg_resolution_index >= 4.5 and avg_resolution_index <= 6:
                        HD_list.append((basename, avg_resolution_index))

            print("")

    return LD_list, SD_list, HD_list


# main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("please input the logs dir path.")
        sys.exit(1)
    logs_dir = sys.argv[1]
    LD_list, SD_list, HD_list = class_resolution_index(logs_dir)
    print(f"LD_list len: {len(LD_list)}")
    print(f"SD_list len: {len(SD_list)}")
    print(f"HD_list len: {len(HD_list)}")
    # print("LD_list: ", LD_list)
    # print("SD_list: ", SD_list)
    # print("HD_list: ", HD_list)

    # write to file
    with open('LD_list.txt', 'w') as f:
        for item in LD_list:
            f.write(f"{item[0]} {item[1]}\n")
    with open('SD_list.txt', 'w') as f:
        for item in SD_list:
            f.write(f"{item[0]} {item[1]}\n")
    with open('HD_list.txt', 'w') as f:
        for item in HD_list:
            f.write(f"{item[0]} {item[1]}\n")