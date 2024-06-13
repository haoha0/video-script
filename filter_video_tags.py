import json

tags_list = []

# 读取json文件，存入tags_list
with open('video_zone_tags_list.json', 'r') as file:
    tags_list = json.load(file)

# 处理tags，筛选出每个分区的热门标签的tag_name和tag_id
tags_list_filtered = []
for tags in tags_list:
    if tags['tags']:    # 如果tags不为空
        print("tags rid: ", tags['rid'])
        tags_filtered = []
        for tag in tags['tags']:
            tags_filtered.append({
                'tag_name': tag['tag_name'],
                'tag_id': tag['tag_id']
            })
        print(len(tags_filtered))  # 输出每个分区的热门标签数量
        tags_list_filtered.append(tags_filtered)

print("tags_list_filtered len: ", len(tags_list_filtered))

# 存入新的json
with open('video_zone_tags_list_filtered.json', 'w', encoding='utf-8') as file:
    json.dump(tags_list_filtered, file, indent=4, ensure_ascii=False)
    print("字典已以 JSON 格式写入文件")

