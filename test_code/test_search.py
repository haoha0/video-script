# 搜索测试
from bilibili_api import search, sync, video_zone
import json

# api提供了一些搜索函数
# search(keyword) 只指定搜索关键词，这个好像会搜出一堆奇奇怪怪的东西，不如指定搜索类型为video
async def test_f_search_by_order():
    return await search.search_by_type("小马宝莉", search_type=search.SearchObjectType.VIDEO,
                                       order_type=search.OrderVideo.TOTALRANK, time_range=10,
                                       page=1, page_size=10, debug_param_func=print)

res = sync(test_f_search_by_order())
# print(res)
print(type(res))
print(len(res['result']))

# 将result中的每个元素的"bvid"存储到列表中
result = res['result']
bvid_list = []
for element in result:
    bvid_list.append(element['bvid'])

print(bvid_list)
print(len(bvid_list))

# 将结果以 JSON 格式写入文件
with open('output_no_video_zone_type_pagesize10.json', 'w') as file:
    json.dump(res, file, indent=4)  # 美化输出
    print("字典已以 JSON 格式写入文件")