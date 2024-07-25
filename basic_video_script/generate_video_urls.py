import json

# 读取json文件
with open('video_bivids_filtered.json', 'r', encoding='utf-8') as file:
    bvids_list = json.load(file)

video_urls = []

# 手动筛选出垃圾视频，竖屏，劣质内容等
waste_videos = ['BV1h7421d72b', 'BV1Mm421K7Ph', 'BV1Lr421s7fF', 'BV1Mr421c7og', 'BV1Mw4m1m7TE',
                'BV1pn4y197hv', 'BV1UB4y1N7zB', 'BV1VG411B7RP', 'BV1vW421P74D', 'BV1Wx4y1e7h8',
                'BV1YT421v7Pi']

for item in bvids_list[:10]:
        tag = item['tag_name']
        id = item['id']
        # print(f' {tag} 标签下的视频')
        for bvid in item['bvid_list']:
            if bvid in waste_videos:    # 跳过垃圾视频
                continue
            # print(bvid)
            video_url = f'f\'http://{{server_ip}}/{bvid}.mpd\','
            video_urls.append(video_url)

# 去重
video_urls = list(set(video_urls))

# 存储到txt
with open('new_video_urls.txt', 'w') as f:
    count = 0
    for url in video_urls:
        f.write(url + '\n')
        count += 1
        separator = '--- End of batch ' + str(count / 10) + ' ---\n'
        if count % 10 == 0:
            f.write(separator + '\n')
            