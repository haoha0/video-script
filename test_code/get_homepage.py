# 获取主页视频，30个，每次获取都会刷新，不重复
from bilibili_api import homepage, hot, sync
import json

res = sync(homepage.get_videos())
print(len(res['item']))

with open('output_homepage.json', 'w') as file:
    json.dump(res, file, indent=4)
    print("字典已以 JSON 格式写入文件")