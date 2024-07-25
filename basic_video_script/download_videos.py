# 下载视频
# SESSDATA
# 93fcc1d8%2C1733098886%2Ce1ab2%2A62CjDt92lRUaFr-kg9BxyR9vfTIXp-FN2PRW__bLtCHVrZyf0Wh9xOE4LEK9vkh2z1aG4SVjRJNHFoUkFUdHFocGdFS3J6dl9Zd29HUWFBQ2dLWnBmNkg3RnFvZ0ZmdTF4ZF8yQk9IOUdNV0FucVl4WmVDVGlCXzhIV1J0S0ljNEMxZ1dXcHJaUURRIIEC
# BILI_JCT
# 52cea7d4be3a72721ea0f328e2d631e0
# BUVID3
# 68386A9C-2C7E-4323-8A3F-DC38A3C09604167643infoc

# 只能下载到对应BV号可以拿到的最高分辨率
# 一些需要会员的可能无法下载
import asyncio
from bilibili_api import video, Credential, HEADERS
import httpx
import os
import json

SESSDATA = "93fcc1d8%2C1733098886%2Ce1ab2%2A62CjDt92lRUaFr-kg9BxyR9vfTIXp-FN2PRW__bLtCHVrZyf0Wh9xOE4LEK9vkh2z1aG4SVjRJNHFoUkFUdHFocGdFS3J6dl9Zd29HUWFBQ2dLWnBmNkg3RnFvZ0ZmdTF4ZF8yQk9IOUdNV0FucVl4WmVDVGlCXzhIV1J0S0ljNEMxZ1dXcHJaUURRIIEC"
BILI_JCT = "52cea7d4be3a72721ea0f328e2d631e0"
BUVID3 = "68386A9C-2C7E-4323-8A3F-DC38A3C09604167643infoc"

# FFMPEG 路径，查看：http://ffmpeg.org/
FFMPEG_PATH = "/opt/homebrew/bin/ffmpeg"

# 读取json文件
with open('video_bivids_filtered.json', 'r') as file:
    bvids_list = json.load(file)

# bvids_list = [
#     {
#         "tag_name": "新番介绍",
#         "bvid_list": [
#             "BV1Df4y1s7rG",
#             "BV1Lc411U7TT"
#         ],
#         "id": 1
#     },
#     {
#         "tag_name": "预告片",
#         "bvid_list": [
#             "BV1ar421A7jx"
#         ],
#         "id": 2
#     }
# ]

async def download_url(url: str, out: str, info: str):
    # 下载函数
    async with httpx.AsyncClient(headers=HEADERS) as sess:
        resp = await sess.get(url)
        length = resp.headers.get('content-length')
        with open(out, 'wb') as f:
            process = 0
            for chunk in resp.iter_bytes(1024):
                if not chunk:
                    break

                process += len(chunk)
                print(f'下载 {info} {process} / {length}')
                f.write(chunk)

async def download_video(path, bvid, credential):
    # 如果没有path文件夹，则创建
    if not os.path.exists(path):
        os.makedirs(path)
    # 实例化 Video 类
    v = video.Video(bvid=bvid, credential=credential)
    # 获取视频下载链接
    download_url_data = await v.get_download_url(0)
    # 解析视频下载信息
    detecter = video.VideoDownloadURLDataDetecter(data=download_url_data)
    streams = detecter.detect_best_streams()
    # 有 MP4 流 / FLV 流两种可能
    if detecter.check_flv_stream():
        # FLV 流下载
        await download_url(streams[0].url, "flv_temp.flv", "FLV 音视频流")
        # 转换文件格式
        os.system(f'{FFMPEG_PATH} -i flv_temp.flv {path}/{bvid}.mp4')
        # 删除临时文件
        os.remove("flv_temp.flv")
    else:
        # MP4 流下载
        await download_url(streams[0].url, "video_temp.m4s", "视频流")
        await download_url(streams[1].url, "audio_temp.m4s", "音频流")
        # 混流
        os.system(f'{FFMPEG_PATH} -i video_temp.m4s -i audio_temp.m4s -vcodec copy -acodec copy {path}/{bvid}.mp4')
        # 删除临时文件
        os.remove("video_temp.m4s")
        os.remove("audio_temp.m4s")
    print(f'已下载为：{path}/{bvid}.mp4')

async def main():
    # 实例化 Credential 类
    credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
    # 遍历 bvids_list
    print(len(bvids_list))

    for item in bvids_list[:10]:
        tag = item['tag_name']
        id = item['id']
        path = f'./videos/videos{id}'
        print(f'正在下载 {tag} 标签下的视频')
        for bvid in item['bvid_list']:
            print(f'正在下载 {bvid}')
            await download_video(path, bvid, credential)
            await asyncio.sleep(1)  # 每次下载后等待1秒

if __name__ == '__main__':
    # 主入口
    asyncio.run(main())
    # asyncio.get_event_loop().run_until_complete(main())