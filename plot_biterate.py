# liuwenhao 7.17
# read biterate files and plot the percentage of different biterate under different bandwidths

# 读取特征文件，计算比特率的各种值所占比例和比特率的平均值
import os
import pandas as pd
import matplotlib.pyplot as plt

file_paths = []
# 获取所有特征文件的路径
for root, dirs, files in os.walk("features"):
    for file in files:
        if file.endswith(".txt"):
            file_paths.append(os.path.join(root, file))

print(file_paths)

# 读取所有特征文件
datas = []
for file_path in file_paths:
    data = pd.read_csv(file_path, sep=" ", header=None, names=['bitrate', 'time'])
    datas.append(data)

# 计算比特率的各种值所占比例和比特率的平均值
bitrate_counts = []
bitrate_means = []
bitrate_labels_set = set()

for data in datas:
    # 计算比特率的比例并添加到列表中
    counts = data['bitrate'].value_counts(normalize=True) * 100
    bitrate_counts.append(counts)

    # 计算比特率的平均值并添加到列表中
    mean = data['bitrate'].mean()
    bitrate_means.append(mean)

    # 更新比特率标签集合
    bitrate_labels_set.update(counts.index.tolist())

# 将集合转换为列表
bitrate_labels = list(bitrate_labels_set)
print("bitrate labels:", bitrate_labels)

# 为每个比特率分配一个固定的颜色
colors = plt.cm.tab20(range(len(bitrate_labels)))
color_map = dict(zip(bitrate_labels, colors))

# 绘制比例堆叠柱状图
plt.figure(figsize=(12, 8))
# colors = ['blue', 'orange', 'green', 'red', 'purple']

legend_labels = set()

for i in range(len(datas)):
    df = pd.DataFrame(bitrate_counts[i]).reset_index()
    df.columns = ['bitrate', 'percentage']
    # sort
    df = df.sort_values(by='bitrate').reset_index()

    # print(df)
    bottom = 0
    for j in range(len(df)):
        # print(df['bitrate'][j])
        bitrate = df['bitrate'][j]
        color = color_map[bitrate]

        if bitrate not in legend_labels:
            plt.bar(f"File {i + 1}", df['percentage'][j], bottom=bottom, label=bitrate, color=color)
            legend_labels.add(bitrate)  # 添加图例
        else:
            plt.bar(f"File {i + 1}", df['percentage'][j], bottom=bottom, color=color)
            # plt.bar(f"File {i + 1}", df['percentage'][j], bottom=bottom, label=df['bitrate'][j] if i == 0 else "", color=color)

        bottom += df['percentage'][j]
        plt.text(f"File {i + 1}", df['percentage'].cumsum()[j] - df['percentage'][j] / 2, f"{df['bitrate'][j]}: {df['percentage'][j]:.2f}%", ha='center', color='black', fontsize=10)

# 预定义的横坐标标签
x_labels = ['300kbit', '600kbit', '1mbit', '2mbit', '3mbit', '4mbit','5mbit', 'xmbit']
plt.xticks(ticks=range(0, len(datas)), labels=x_labels)

plt.xlabel('Bandwidth (bit/s)')
plt.ylabel('Percentage (%)')
plt.title('Percentage of Different Bitrates')
plt.legend(title='Bitrate (kbps)')
plt.savefig('BV1P44y1F72Z_bitrate1.pdf') # need to be modified
plt.show()