#### reference: 
https://github.com/nemo2011/bilibili-api

#### doc: 
https://nemo2011.github.io/bilibili-api/#/

#### video coding and processing: 
https://blog.csdn.net/LvGreat/article/details/103531277
https://www.twblogs.net/a/5f01fe6f9644181341a1a8ce/

#### gpac:
https://blog.csdn.net/LvGreat/article/details/103588897
https://github.com/gpac/gpac.git


#### 视频下载处理流程：
1. get_video_infos.py: 获取视频信息，生成video_zone_tags_list.json文件，获取所有分区的热门视频标签
2. filter_video_tags.py: 过滤视频标签，生成video_zone_tags_list_filtered.json文件，处理tags，筛选出每个分区的热门标签的tag_name和tag_id
3. get_video_bvids.py: 获取视频bvid，生成video_bvids.json文件，根据每个分区前5个热门标签(tag)进行视频搜索，每个tag搜索综合排序的前10个视频
4. filter_video_bvids.py: 过滤去重bvid，为tag_name添加id(方便后续分别存储)，生成video_bvids_filtered.json文件，上述视频搜索基于tag，tag存在重复，导致视频bvid重复(此处应该优化代码，提前对tag_name进行去重操作 TODO)
5. download_videos.py: 根据video_bivids_filtered.json下载对应bvid的视频
6. transcode_videos.py: 视频转码，生成不同分辨率的视频切片和mpd描述文件
7. fix_mpd.py: # 检查生成的 MPD 文件是否正常，如果不正常则修复


#### 视频播放控制：
1. control_video_player.py: 视频播放控制的基本code (目前基本弃用)
2. inorder_control_video_player.py: 目前主要使用该优化后的代码
3. process_logs.py: 对播放视频产生的原始日志进行处理过滤，筛选重要信息
4. generate_biterates.py: TODO，需要调整优化
5. plot_biterates.py: 根据某一路径下的不同带宽的视频播放分辨率结果绘制比特率百分比柱状图
