# liuwenhao 7.17
# read index files and plot the percentage of different index under different bandwidths

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import re

if len(sys.argv) != 2:
    print("please input the logs dir path.")
    sys.exit(1)
logs_dir = sys.argv[1]

dir_paths = []
file_paths = []

# 获取所有特征文件的路径
for dirpath, dirnames, filenames in os.walk(logs_dir):
    if dirpath.endswith("_index"):
        # TODO
        # print(dirpath)
        dir_paths.append(dirpath)

# 排序
# 定义一个排序函数，用于从目录名中提取排序键
def sort_key(path):
    # 使用正则表达式提取数值和单位
    match = re.search(r"(\d+)([km])bit", path)
    if match:
        num, unit = match.groups()
        num = int(num)
        # 将kbit转换为等效的mbit数值
        if unit == 'k':
            num *= 0.001
        return num, unit == 'k'
    return float('inf'), False  # 如果没有匹配，返回无穷大和False以确保它排在最后

# 使用sorted函数和自定义的排序键对目录进行排序
sorted_dir_paths = sorted(dir_paths, key=sort_key)
# print(sorted_dir_paths)

# 读取所有特征文件
all_datas = []
for dir in sorted_dir_paths:
    print("process dir: ", dir)
    datas = pd.DataFrame()

    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".txt"):
                # file_paths.append(os.path.join(root, file))
                file_path = os.path.join(root, file)
                # data.append(pd.read_csv(file_path, sep=" ", header=None, names=['bitrate', 'time']))
                data = pd.read_csv(file_path, header=None, names=['index'])
                datas = pd.concat([datas, data], ignore_index=True)
    all_datas.append(datas)

# 计算分辨率指数的各种值所占比例和分辨率指数的平均值
index_counts = []
index_means = []
index_labels_set = set()

for item in all_datas:
    # 计算分辨率指数的比例并添加到列表中
    counts = item['index'].value_counts(normalize=True) * 100
    index_counts.append(counts)

    # 计算分辨率指数的平均值并添加到列表中
    mean = item['index'].mean()
    index_means.append(mean)

    # 更新分辨率指数标签集合
    index_labels_set.update(counts.index.tolist())

# 将集合转换为列表
index_labels = list(index_labels_set)

# 为每个分辨率指数分配一个固定的颜色
colors = plt.cm.tab20(range(len(index_labels)))
color_map = dict(zip(index_labels, colors))

# 绘制比例堆叠柱状图
plt.figure(figsize=(12, 8))

legend_labels = set()

for i in range(len(all_datas)):
    df = pd.DataFrame(index_counts[i]).reset_index()
    df.columns = ['index', 'percentage']
    # sort
    df = df.sort_values(by='index').reset_index()

    bottom = 0
    for j in range(len(df)):
        index = df['index'][j]
        color = color_map[index]

        if index not in legend_labels:
            plt.bar(f"File {i + 1}", df['percentage'][j], bottom=bottom, label=index, color=color)
            legend_labels.add(index)  # 添加图例
        else:
            plt.bar(f"File {i + 1}", df['percentage'][j], bottom=bottom, color=color)

        bottom += df['percentage'][j]
        plt.text(f"File {i + 1}", df['percentage'].cumsum()[j] - df['percentage'][j] / 2, f"{df['index'][j]}: {df['percentage'][j]:.2f}%", ha='center', color='black', fontsize=10)

x_labels = ['300kbit', '500kbit', '1mbit', '2mbit', '3mbit', '4mbit','5mbit', 'xmbit']
plt.xticks(ticks=range(0, len(all_datas)), labels=x_labels)

plt.xlabel('Resolution Quality Index')
plt.ylabel('Percentage (%)')
plt.title('Percentage of Different Resolution Quality Index under Different Bandwidths')
plt.legend(title='Index')
plt.savefig('test.pdf') # need to be modified
plt.show()