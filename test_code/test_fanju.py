from bilibili_api import bangumi, sync

# 获取番剧的bv号
async def main():
    ep = bangumi.Episode(374717)
    # 打印 bv 号
    print(ep.get_bvid())

sync(main())