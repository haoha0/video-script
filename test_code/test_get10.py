from bilibili_api import video_zone, sync

tid = [
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
    # video_zone.VideoZoneTypes.INFORMATION.value, # 资讯
    video_zone.VideoZoneTypes.FOOD.value, # 美食
    video_zone.VideoZoneTypes.LIFE.value, # 生活
    video_zone.VideoZoneTypes.CAR.value, # 汽车
    video_zone.VideoZoneTypes.FASHION.value, # 时尚
    video_zone.VideoZoneTypes.SPORTS.value, # 运动
    video_zone.VideoZoneTypes.ANIMAL.value, # 动物圈
    video_zone.VideoZoneTypes.VLOG.value # VLOG
]

# for i in tid:
#     res = sync(video_zone.get_zone_top10(i))
#     print(i)
#     print(type(res))


# res = video_zone.get_zone_list_sub()

# # json
# import json
# with open('test.json', 'w', encoding='utf-8') as file:
#     json.dump(res, file, indent=4, ensure_ascii=False)
#     print("字典已以 JSON 格式写入文件")

res1 = sync(video_zone.get_zone_hot_tags(202))
print(type(res1))

# json
import json
with open('video.json', 'w', encoding='utf-8') as file:
    json.dump(res1, file, indent=4, ensure_ascii=False)
    print("字典已以 JSON 格式写入文件")
