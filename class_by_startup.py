# 遍历给定目录下所有以startup结尾的文件夹，处理文件夹下面的所有txt文件
# 读取每个文件中第一行的两个数字，计算后者－前者，得到startup时间


# usage: python class_by_startup.py logs_dir
# eg: python3 .\class_by_startup.py ..\..\output_data\logs\0801_ground_logs\

# 10.9: python3 .\class_by_startup.py ..\..\output_data\plotinus_logs\1005_logs_startup_test

import os
import sys

# return: file basename and startup time
# def read_index(file_path):
#     with open(file_path, 'r') as f:
#         lines = f.readlines()

#     resolution_index = sum(int(line) for line in lines) / len(lines)
#     basename = '_'.join(os.path.basename(file_path).split('_')[:-1])

#     return basename, resolution_index

def read_startup(file_path):
    # 读第一行，第一行有两个数字，空格隔开
    with open(file_path, 'r') as f:
        basename = '_'.join(os.path.basename(file_path).split('_')[:-1])
        line = f.readline()

        # 视频未播放，返回最大startup
        if len(line.split()) < 2:
            # print("not play. \n")
            startup_time = 30
            return basename, startup_time
        
        # 视频播放，返回startup时间
        time1 = float(line.split()[0])
        time2 = float(line.split()[1])
        startup_time = (time2 - time1) / 1000

    return basename, startup_time



def class_startup(logs_dir):
    # 三分类
    # quick_started_list = []
    # slow_started_list = []
    # not_started_list = []

    # 二分类
    Started_list = []
    Not_started_list = []

    dirs = os.listdir(logs_dir) # 列出指定目录下的所有文件和目录名，返回的是一个列表
    for dir in dirs:
        if dir.endswith('startup'):
            print("processing dir: ", dir)
            dir_path = os.path.join(logs_dir, dir)

            for file in os.listdir(dir_path):
                if file.endswith('txt'):
                    print("processing file: ", file)
                    file_path = os.path.join(dir_path, file)
                    
                    # basename, avg_resolution_index = read_index(file_path)
                    # print("basename: ", basename, " avg resolution index: ", avg_resolution_index)

                    basename, startup_time = read_startup(file_path)
                    print("basename: ", basename, " startup time: ", startup_time)

                    # 三分类
                    # if startup_time < 1:
                    #     quick_started_list.append((basename, startup_time))
                    # elif startup_time >= 1 and startup_time < 10:
                    #     slow_started_list.append((basename, startup_time))
                    # elif startup_time >= 10:
                    #     not_started_list.append((basename, startup_time))

                    # 二分类：
                    if startup_time < 10:
                        Started_list.append((basename, startup_time))
                    else:
                        Not_started_list.append((basename, startup_time))

            print("")

    # return quick_started_list, slow_started_list, not_started_list
    return Started_list, Not_started_list


# main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("please input the logs dir path.")
        sys.exit(1)
    logs_dir = sys.argv[1]

    # 三分类
    # quick_started_list, slow_started_list, not_started_list = class_startup(logs_dir)
    # print("quick_started_list: ", len(quick_started_list))
    # print("slow_started_list: ", len(slow_started_list))
    # print("not_started_list: ", len(not_started_list))
    # print("quick_started_list: ", quick_started_list)
    # print("slow_started_list: ", slow_started_list)
    # print("not_started_list: ", not_started_list)

    # with open('quick_started_list.txt', 'w') as f:
    #     for item in quick_started_list:
    #         f.write(f"{item[0]} {item[1]}\n")
    # with open('slow_started_list.txt', 'w') as f:
    #     for item in slow_started_list:
    #         f.write(f"{item[0]} {item[1]}\n")
    # with open('not_started_list.txt', 'w') as f:
    #     for item in not_started_list:
    #         f.write(f"{item[0]} {item[1]}\n")

    # 二分类
    Started_list, Not_started_list = class_startup(logs_dir)
    print("Started_list: ", len(Started_list))
    print("Not_started_list: ", len(Not_started_list))
    # print("Started_list: ", Started_list)
    # print("Not_started_list: ", Not_started_list)

    with open('plotinus_static/new_startup/started.txt', 'w') as f:
        for item in Started_list:
            f.write(f"{item[0]} {item[1]}\n")
    with open('plotinus_static/new_startup/not_started.txt', 'w') as f:
        for item in Not_started_list:
            f.write(f"{item[0]} {item[1]}\n")
