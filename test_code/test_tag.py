from bilibili_api import video_tag, sync

tag = video_tag.Tag(tag_id=1762404)

res = sync(tag.get_tag_info())

# res = sync(video_tag.Tag.get_tag_info(683752))

print(res)