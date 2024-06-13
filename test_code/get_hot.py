from bilibili_api import hot, sync
import json

# # 获取热门内的综合热门视频，20个，有bvid，对应热门中的综合热门
# res_hot = sync(hot.get_hot_videos())
# print(len(res_hot['list']))
# # json
# with open('output_hot.json', 'w') as file:
#     json.dump(res_hot, file, indent=4)
#     print("字典已以 JSON 格式写入文件")

# 获取每周必看列表(仅概述)
# res_weekly = sync(hot.get_weekly_hot_videos_list())
# print(len(res_weekly['list']))
# # json
# with open('output_weekly.json', 'w') as file:
#     json.dump(res_weekly, file, indent=4)
#     print("字典已以 JSON 格式写入文件")
# return 感觉没啥用
# {
#     "number": 4,
#     "subject": "\u5df4\u9ece\u5723\u6bcd\u9662",
#     "status": 2,
#     "name": "2019\u7b2c4\u671f 04.12 - 04.18"
# },

# 获取热词图鉴信息
# return 返回一些网络热词，感觉没啥用
# res_hot_buzzwords = sync(hot.get_hot_buzzwords())
# print(len(res_hot_buzzwords['buzzwords']))
# # json
# with open('output_hot_buzzwords.json', 'w', encoding='utf-8') as file:
#     json.dump(res_hot_buzzwords, file, ensure_ascii=False, indent=4)
#     print("字典已以 JSON 格式写入文件")
