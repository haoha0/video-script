# 遍历给定目录下所有以startup结尾的文件夹，处理文件夹下面的所有txt文件
# 读取每个文件中的行数，如果行数大于1，则说明存在重缓冲事件


# usage: python class_by_buffer.py logs_dir
# eg: python3 .\class_by_buffer.py ..\..\output_data\logs\0801_ground_logs\

import os
import sys

def read_buffer(file_path):
    # 读第一行，第一行有两个数字，空格隔开
    with open(file_path, 'r') as f:
        basename = '_'.join(os.path.basename(file_path).split('_')[:-1])
        
        # 计算行数
        lines = f.readlines()
        buffer_count = len(lines) - 1

    return basename, buffer_count


def class_buffer(logs_dir):
    # 二分类
    Buffer_list = []
    Not_buffer_list = []

    dirs = os.listdir(logs_dir) # 列出指定目录下的所有文件和目录名，返回的是一个列表
    for dir in dirs:
        if dir.endswith('startup'):
            print("processing dir: ", dir)
            dir_path = os.path.join(logs_dir, dir)

            for file in os.listdir(dir_path):
                if file.endswith('txt'):
                    print("processing file: ", file)
                    file_path = os.path.join(dir_path, file)

                    basename, buffer_count = read_buffer(file_path)
                    print("basename: ", basename, " buffer count: ", buffer_count)

                    # 二分类：
                    if buffer_count > 1:
                        Buffer_list.append((basename, buffer_count))
                    else:
                        Not_buffer_list.append((basename, buffer_count))

            print("")

    return Buffer_list, Not_buffer_list


# main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("please input the logs dir path.")
        sys.exit(1)
    logs_dir = sys.argv[1]

    # 二分类
    Started_list, Not_started_list = class_buffer(logs_dir)
    print("Buffer_list: ", len(Started_list))
    print("Not_buffer_list: ", len(Not_started_list))

    with open('Buffer.txt', 'w') as f:
        for item in Started_list:
            f.write(f"{item[0]} {item[1]}\n")
    with open('Not_buffer.txt', 'w') as f:
        for item in Not_started_list:
            f.write(f"{item[0]} {item[1]}\n")
