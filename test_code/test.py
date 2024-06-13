from bilibili_api import search, sync, video_tag

res = sync(search.search("奥利给"))

# json
import json
with open('test.json', 'w') as file:
    json.dump(res, file, indent=4)
    print("字典已以 JSON 格式写入文件")
