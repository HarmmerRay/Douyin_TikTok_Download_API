class KsWebCrawler:

    async def fetch_user_profile(self,user_id:str):
        return "fetch_user_profile"

    async def fetch_live_playbacks(self,user_id:str):
        return "fetch_live_playbacks"

    async def fetch_playback_info(self,product_id:str):
        return "fetch_playback_info"

    async def fetch_works_list(self,user_id:str):
        return "fetch_works_list"

    async def fetch_work_comment_list(self,photo_id:str):
        return "fetch_work_comment_list"
