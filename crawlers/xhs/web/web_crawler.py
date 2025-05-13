# 配置文件路径
import os
import re

import yaml
import time  # 时间操作
import asyncio  # 异步I/O

from lxml import html

from crawlers.base_crawler import BaseCrawler
from crawlers.xhs.web.utils import extract_initial_state_xpath

path = os.path.abspath(os.path.dirname(__file__))

# 读取配置文件
with open(f"{path}/config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

class XhsWebCrawler:
    async def get_xhs_header(self):
        xhs_config = config["xhs"]
        kwargs = {
            "headers":{
                "User-Agent":xhs_config["headers"]["User-Agent"],
                "Cookie":xhs_config["headers"]["Cookie"]
            },
            "proxies": {"http://": xhs_config["proxies"]["http"],"https://": xhs_config["proxies"]["https"]},
        }
        return kwargs
    # handler接口列表
    async def fetch_one_video(self,url: str):
        # 获取小红书实时cookie
        kwargs = await self.get_xhs_header()
        # 创建一个基础爬虫
        base_crawler = BaseCrawler(proxies=kwargs["proxies"],crawler_headers=kwargs["headers"])
        async with base_crawler as crawler:  #保证异步操作中 操作句柄/网络连接等资源被释放
            # n cookie 对应 一个作品 对应 n xsec_token  只要有一个cookie 和 xsec_token 就可以拿到数据。
            response = await crawler.get_fetch_data(url)
        # print(response.text)
        response = await extract_initial_state_xpath(response.text)

        # print(response)
        return response
        

    async def fetch_one_note(self,note_id: str):
        return "fetch_one_note"

    async def fetch_first_level_comment(self,note_id: str):
        return "fetch_first_level_comment"

    async def fetch_second_level_comment(self,note_id: str,comment_id:str):
        return "fetch_second_level_comment"


    async def main(self):
        # 获取单一视频笔记信息
        url = "https://www.xiaohongshu.com/explore/6809acdd000000001202c014?xsec_token=AB0562f9vQnINi-bglZrC4hIq3pQe1E9yM5ucnzCHF3OU=&xsec_source=pc_search&source=web_search_result_notes"
        result = await self.fetch_one_video(url)
        print(result)

if __name__ == "__main__":
    crawler = XhsWebCrawler()
    # 开始时间
    start = time.time()
    asyncio.run(crawler.main())
    end = time.time()
    print(f"耗时：{end - start}")