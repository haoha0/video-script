from bilibili_api import video_zone, sync
import json

# 选定视频分区
"""
    所有分区枚举
    - ANIME: 番剧
    - MOVIE: 电影
    - GUOCHUANG: 国创
    - TELEPLAY: 电视剧
    - DOCUMENTARY: 纪录片
    - DOUGA: 动画
    - GAME: 游戏
    - KICHIKU: 鬼畜
    - MUSIC: 音乐
    - DANCE: 舞蹈
    - CINEPHILE: 影视
    - ENT: 娱乐
    - KNOWLEDGE: 知识
    - TECH: 科技
    - INFORMATION: 资讯
    - FOOD: 美食
    - LIFE: 生活
    - CAR: 汽车
    - FASHION: 时尚
    - SPORTS: 运动
    - ANIMAL: 动物圈
    - VLOG: VLOG
"""
tid_list = [
    video_zone.VideoZoneTypes.ANIME.value, # 番剧
    video_zone.VideoZoneTypes.MOVIE.value, # 电影
    video_zone.VideoZoneTypes.GUOCHUANG.value, # 国创
    video_zone.VideoZoneTypes.TELEPLAY.value, # 电视剧
    video_zone.VideoZoneTypes.DOCUMENTARY.value, # 纪录片
    video_zone.VideoZoneTypes.DOUGA.value, # 动画
    video_zone.VideoZoneTypes.GAME.value, # 游戏
    video_zone.VideoZoneTypes.KICHIKU.value, # 鬼畜
    video_zone.VideoZoneTypes.MUSIC.value, # 音乐
    video_zone.VideoZoneTypes.DANCE.value, # 舞蹈
    video_zone.VideoZoneTypes.CINEPHILE.value, # 影视
    video_zone.VideoZoneTypes.ENT.value, # 娱乐
    video_zone.VideoZoneTypes.KNOWLEDGE.value, # 知识
    video_zone.VideoZoneTypes.TECH.value, # 科技
    video_zone.VideoZoneTypes.INFORMATION.value, # 资讯
    video_zone.VideoZoneTypes.FOOD.value, # 美食
    video_zone.VideoZoneTypes.LIFE.value, # 生活
    video_zone.VideoZoneTypes.CAR.value, # 汽车
    video_zone.VideoZoneTypes.FASHION.value, # 时尚
    video_zone.VideoZoneTypes.SPORTS.value, # 运动
    video_zone.VideoZoneTypes.ANIMAL.value, # 动物圈
    video_zone.VideoZoneTypes.VLOG.value # VLOG
]

# 获取分区信息，热门标签，top10视频
info_list = []
tags_list = []
top10_list = []

for tid in tid_list:
    print("收集tid为{}的分区信息，热门标签，top10视频".format(tid))
    info = video_zone.get_zone_info_by_tid(tid)
    tags = sync(video_zone.get_zone_hot_tags(tid))
    if tid != 202:  # 异常分区
        videos = sync(video_zone.get_zone_top10(tid))

    info_list.append(info)
    tags_list.append(tags)
    top10_list.append(videos)

print("tags_list len: ", len(tags_list))

# info
with open('video_zone_info_list.json', 'w', encoding='utf-8') as file:
    json.dump(info_list, file, indent=4, ensure_ascii=False)
    print("所有分区信息已以 JSON 格式写入文件")

# tags  haohao: 产生分区热门标签列表
with open('video_zone_tags_list.json', 'w', encoding='utf-8') as file:
    json.dump(tags_list, file, indent=4, ensure_ascii=False)
    print("所有分区热门标签已以 JSON 格式写入文件")

# top10
with open('video_zone_top10_list.json', 'w', encoding='utf-8') as file:
    json.dump(top10_list, file, indent=4, ensure_ascii=False)
    print("所有分区top10视频已以 JSON 格式写入文件")