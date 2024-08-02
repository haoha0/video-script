# 遍历给定目录下所有以bitrates结尾的文件夹，处理文件夹下面的所有txt文件

# 每个txt文件中为一次视频播放每个时刻的比特率，每一行为两个数字，分别为比特率和时间

# 计算每个视频播放的平均比特率，根据所有的平均比特率范围设定三个比特率区间，分别为LD、SD、HD
# 根据分布划分三个区间
# LD: [0, 500)
# SD: [500, 1500)
# HD: [1500, +∞)

# 设定视频质量等级对应的三个list，存储每个视频对应文件的base name和平均比特率

# 计算每个视频播放的平均比特率，划分到对应的区间

# usage: python3 class_by_bitrate.py logs_dir
# eg: python3 class_by_bitrate.py ..\..\pcap_data\0724_ground_logs_test_bitrates
import os
import sys
import re

# return: file basename and avg resolution index
def read_bitrates(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    bitrates = [int(line.split()[0]) for line in lines] # 取出每行的比特率
    avg_bitrate = sum(bitrates) / len(bitrates)
    basename = '_'.join(os.path.basename(file_path).split('_')[:-1])  

    return basename, avg_bitrate 


# 生成所有视频的比特率分布
# def generate_bitrates_range(logs_dir):
#     all_bitrates = []

#     dirs = os.listdir(logs_dir) # 列出指定目录下的所有文件和目录名，返回的是一个列表
#     for dir in dirs:
#         if dir.endswith('bitrates'):
#             print("processing dir: ", dir)
#             dir_path = os.path.join(logs_dir, dir)

#             for file in os.listdir(dir_path):
#                 if file.endswith('txt'):
#                     print("calculating bitrate of:  ", file)
#                     file_path = os.path.join(dir_path, file)
                    
#                     basename, avg_bitrate = read_bitrates(file_path)
#                     print("basename: ", basename, " avg bitrate: ", avg_bitrate)
#                     all_bitrates.append(avg_bitrate)

    # print("all_bitrates: ", all_bitrates)
    # print(len(all_bitrates))
    # 绘制all_bitrates的分布图
    # import matplotlib.pyplot as plt
    # import numpy as np
    # plt.hist(all_bitrates, bins=100, color='steelblue', edgecolor='k')
    # plt.xlabel('bitrate')
    # plt.ylabel('count')
    # plt.title('bitrates distribution')
    # plt.savefig('bitrates_distribution.png')
    # plt.show()



def class_bitrate(logs_dir):
    LD_list = []
    SD_list = []
    HD_list = []

    dirs = os.listdir(logs_dir) # 列出指定目录下的所有文件和目录名，返回的是一个列表
    for dir in dirs:
        if dir.endswith('bitrates'):
            print("processing dir: ", dir)
            dir_path = os.path.join(logs_dir, dir)

            for file in os.listdir(dir_path):
                if file.endswith('txt'):
                    print("processing file: ", file)
                    file_path = os.path.join(dir_path, file)
                    
                    basename, avg_bitrate = read_bitrates(file_path)
                    print("basename: ", basename, " avg bitrate: ", avg_bitrate)

                    # 划分到对应的区间
                    if avg_bitrate >= 0 and avg_bitrate < 500:
                        LD_list.append((basename, avg_bitrate))
                    elif avg_bitrate >= 500 and avg_bitrate < 1500:
                        SD_list.append((basename, avg_bitrate))
                    elif avg_bitrate >= 1500:
                        HD_list.append((basename, avg_bitrate))

            print("")

    return LD_list, SD_list, HD_list


# main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("please input the logs dir path.")
        sys.exit(1)
    logs_dir = sys.argv[1]


    LD_list, SD_list, HD_list = class_bitrate(logs_dir)
    print(f"LD_list len: {len(LD_list)}")
    print(f"SD_list len: {len(SD_list)}")
    print(f"HD_list len: {len(HD_list)}")

    # print("LD_list: ", LD_list)
    # print("SD_list: ", SD_list)
    # print("HD_list: ", HD_list)

    # # write to file
    with open('bitrate_LD_list.txt', 'w') as f:
        for item in LD_list:
            f.write(f"{item[0]} {item[1]}\n")
    with open('bitrate_SD_list.txt', 'w') as f:
        for item in SD_list:
            f.write(f"{item[0]} {item[1]}\n")
    with open('bitrate_HD_list.txt', 'w') as f:
        for item in HD_list:
            f.write(f"{item[0]} {item[1]}\n")