import json

# 读取json文件
with open('video_bivids_filtered.json', 'r') as file:
    bvids_list = json.load(file)

video_urls = []

for item in bvids_list[:10]:
        tag = item['tag_name']
        id = item['id']
        # print(f' {tag} 标签下的视频')
        for bvid in item['bvid_list']:
            video_url = f'\'http://123.57.76.186/{bvid}.mpd\','
            video_urls.append(video_url)

# 去重
video_urls = list(set(video_urls))

# 存储到txt
with open('video_urls.txt', 'w') as f:
    count = 0
    for url in video_urls:
        f.write(url + '\n')
        count += 1
        separator = '--- End of batch ' + str(count / 10) + ' ---\n'
        if count % 10 == 0:
            f.write(separator + '\n')
            