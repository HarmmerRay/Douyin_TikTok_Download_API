class XhsWebCrawler:

    # handler接口列表
    async def fetch_one_video(self,note_id: str):
        return "fetch_one_video"

    async def fetch_one_note(self,note_id: str):
        return "fetch_one_note"

    async def fetch_first_level_comment(self,note_id: str):
        return "fetch_first_level_comment"

    async def fetch_second_level_comment(self,note_id: str,comment_id:str):
        return "fetch_second_level_comment"