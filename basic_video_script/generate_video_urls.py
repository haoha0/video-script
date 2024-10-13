import json

# 读取json文件
with open('../basic_video_infos/video_bivids_filtered.json', 'r', encoding='utf-8') as file:
    bvids_list = json.load(file)

# print(len(bvids_list))
video_urls = []

# 手动筛选出垃圾视频，竖屏，劣质内容等
waste_videos = ['BV1h7421d72b', 'BV1Mm421K7Ph', 'BV1Lr421s7fF', 'BV1Mr421c7og', 'BV1Mw4m1m7TE',
                'BV1pn4y197hv', 'BV1UB4y1N7zB', 'BV1VG411B7RP', 'BV1vW421P74D', 'BV1Wx4y1e7h8',
                'BV1YT421v7Pi', 'BV1mT421Q7Zs', 'BV1j7421o7wd', 'BV1Aa4y1a7mW', 'BV1dH4y1u7Ga']

less_2min = ['BV1EY411d77Z', 'BV1Mr421p7W4', 'BV1rj411J7sN', 'BV11N4y197Ng', 'BV14m421N7Q5',
             'BV1Dr421u7fQ', 'BV1Lr421s7fF', 'BV1Mr421c7og', 'BV1Np4y157Gs',
             'BV1ks411W7r5', 'BV1mm421N7b1', 'BV1rm42157NK',
             'BV1qv4y1p7YN', 'BV1w84y1t7ah',
             'BV1a24y1j74Z', 'BV1BV4y1T769',
             'BV1ai421D7yu', 'BV1Br421w7Pz', 'BV1pz421a7oC', 'BV1zi421S7QJ',
             'BV1Sp4y1j78N', 'BV1te4y1E7K5', 'BV16Y4y13724',
             'BV1Am421K7LM', 'BV1Sf421Q7vU', 'BV1Vm421T7zL', 'BV1YT421v7Pi']

for item in bvids_list[:10]:
        tag = item['tag_name']
        id = item['id']
        # print(f' {tag} 标签下的视频')
        for bvid in item['bvid_list']:
            if bvid in waste_videos or bvid in less_2min:    # 跳过垃圾视频
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
            