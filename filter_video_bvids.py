import json

# 读取 JSON 文件
with open('video_bvids.json', 'r') as file:
    bvid_list = json.load(file)

print("原list数据长度：", len(bvid_list))

# 使用集合记录已出现的 tag_name
seen_tags = set()
filtered_bvid_list = []
currnet_id = 1

for item in bvid_list:
    tag_name = item['tag_name']
    if tag_name not in seen_tags:
        # 添加递增的id
        item['id'] = currnet_id
        filtered_bvid_list.append(item)
        seen_tags.add(tag_name)
        currnet_id += 1
    else:
        print(f"Duplicate tag_name: {tag_name}")

# 将结果写入新的 JSON 文件
with open('video_bivids_filtered.json', 'w', encoding='utf-8') as file:
    json.dump(filtered_bvid_list, file, indent=4, ensure_ascii=False)

print("已将去重后的结果写入 'filtered_video_zone_tags_list.json'")
print("新list数据长度：", len(filtered_bvid_list))
