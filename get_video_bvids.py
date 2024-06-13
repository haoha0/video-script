from bilibili_api import search, sync
import json
import asyncio

# 根据tags进行视频搜索
tags_list = []
with open('video_zone_tags_list_filtered.json', 'r') as file:
    tags_list = json.load(file)

# 截取每个分区的前5个tag_name，存入all_tags_name
tag_names = []
for tags in tags_list:
    for tag in tags[:5]:
        tag_names.append(tag['tag_name'])

print(len(tag_names))
print(tag_names)

# 根据tag_name搜索视频
# 定义一个异步函数来搜索每个标签，并返回视频的bvid
async def search_videos_by_tag(tag_name):
    try:
        results = await search.search_by_type(tag_name, search_type=search.SearchObjectType.VIDEO,
                                            order_type=search.OrderVideo.TOTALRANK, time_range=10,
                                            page=1, page_size=10, debug_param_func=print)
        return results['result']
    except Exception as e:
        print(f"Error searching for tag {tag_name}: {e}")
        return []

# 循环遍历所有标签，搜索视频并收集bvid
bvids_list = []
async def process(tag_names):
    for tag_name in tag_names:
        result = await search_videos_by_tag(tag_name)
        bvid_list = [video['bvid'] for video in result]
        print(len(bvid_list))
        bvids_list.append({'tag_name': tag_name, 'bvid_list': bvid_list})
        await asyncio.sleep(1)  # 添加1秒的延迟，防止请求过快

# 运行异步函数
sync(process(tag_names))

# 输出结果
print(len(bvids_list))
print(bvids_list)

# 将结果以 JSON 格式写入文件
with open('video_bvids.json', 'w', encoding='utf-8') as file:
    json.dump(bvids_list, file, indent=4, ensure_ascii=False)  # 美化输出
    print("字典已以 JSON 格式写入文件")