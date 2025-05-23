# 配置文件路径
import os
import re

import yaml
import time  # 时间操作
import asyncio  # 异步I/O

from lxml import html

from crawlers.base_crawler import BaseCrawler
from crawlers.xhs.web.utils import extract_video_info, extract_note_info

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
        response = await extract_video_info(response.text)
        # print(response)
        return response
        

    async def fetch_one_note(self,url: str):
        # 获取小红书实时cookie
        kwargs = await self.get_xhs_header()
        # 创建一个基础爬虫
        base_crawler = BaseCrawler(proxies=kwargs["proxies"], crawler_headers=kwargs["headers"])
        async with base_crawler as crawler:  # 保证异步操作中 操作句柄/网络连接等资源被释放
            # n cookie 对应 一个作品 对应 n xsec_token  只要有一个cookie 和 xsec_token 就可以拿到数据。
            response = await crawler.get_fetch_data(url)
        # print(response.text)
        response = await extract_note_info(response.text)
        # print(response)
        return response

    async def fetch_first_level_comment(self,note_id: str,xsec_token: str):
        kwargs = await self.get_xhs_header()
        base_crawler = BaseCrawler(proxies=kwargs["proxies"], crawler_headers=kwargs["headers"])
        async with base_crawler as crawler:  # 保证异步操作中 操作句柄/网络连接等资源被释放
            # n cookie 对应 一个作品 对应 n xsec_token  只要有一个cookie 和 xsec_token 就可以拿到数据。
            first_level_comments_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?"
            first_level_comments_url = first_level_comments_url + "note_id=" + note_id + "&xsec_token=" + xsec_token + "&cursor=&top_comment_id=&image_formats=jpg,webp,avif"
            print(first_level_comments_url)
            response = await crawler.fetch_get_json(first_level_comments_url)
        # print(response.text)
        # response = await extract_note_info(response.text)
        # print(response)
        return response

    async def fetch_second_level_comment(self,note_id: str,comment_id:str):
        return "fetch_second_level_comment"


    async def main(self):
        # {"global": {"appSettings": {"notificationInterval": 30, "prefetchTimeout": 3001, "prefetchRedisExpires": 259200000, "searchFilterGuideConfig": {"maxDailyShow": 1, "maxTotalShow": 3, "showInterval": 1, "validDays": 15, "autoCloseDelay": 5000}, "retryFeeds": true, "grayModeConfig": {"global": false, "dateRange": ["2023-08-01 00:00:00", "2023-08-19 23:59:59"], "greyRule": {"layout": {"enable": false, "pages": ["Explore"]}, "pages": ["Explore"]}, "disableLikeNotes": ["64ce36f7000000000c036ba5"], "disableSearchHint": false}, "NIO": true, "ICPInfoList": [{"label": "\u6caaICP\u590713030189\u53f7", "link": "//beian.miit.gov.cn/", "title": "\u5c0f\u7ea2\u4e66_\u6caaICP\u5907"}, {"label": "\u8425\u4e1a\u6267\u7167", "link": "//fe-video-qc.xhscdn.com/fe-platform/5581076bd6b6af2e0e943abb024ad0e16f2ebff6.pdf", "title": "\u5c0f\u7ea2\u4e66_\u8425\u4e1a\u6267\u7167"}, {"label": "2024\u6caa\u516c\u7f51\u5b89\u590731010102002533\u53f7", "link": "//www.beian.gov.cn/portal/registerSystemInfo?recordcode=31010102002533", "title": "\u5c0f\u7ea2\u4e66_\u6caa\u516c\u7f51\u5b89\u5907"}, {"label": "\u589e\u503c\u7535\u4fe1\u4e1a\u52a1\u7ecf\u8425\u8bb8\u53ef\u8bc1\uff1a\u6caaB2-20150021", "link": "//fe-video-qc.xhscdn.com/fe-platform/0af4fdb25bbbf95b4adcf32f7aab5f9ea0281316/%E8%A1%8C%E5%90%9F%E4%B8%8A%E6%B5%B7-%E5%A2%9E%E5%80%BC%E7%94%B5%E4%BF%A1%E4%B8%9A%E5%8A%A1%E7%BB%8F%E8%90%A5%E8%AE%B8%E5%8F%AF%E8%AF%81-%E5%85%AC%E7%A4%BA.pdf", "title": "\u5c0f\u7ea2\u4e66_\u7f51\u6587"}, {"label": "\u533b\u7597\u5668\u68b0\u7f51\u7edc\u4ea4\u6613\u670d\u52a1\u7b2c\u4e09\u65b9\u5e73\u53f0\u5907\u6848\uff1a(\u6caa)\u7f51\u68b0\u5e73\u53f0\u5907\u5b57[2019]\u7b2c00006\u53f7", "link": "//fe-video-qc.xhscdn.com/fe-platform/410dce57bc12a6d7e5808060e47644fbe46f68ff.pdf", "title": "\u5c0f\u7ea2\u4e66_\u533b\u7597\u5668\u68b0\u7f51\u7edc\u4ea4\u6613\u670d\u52a1"}, {"label": "\u4e92\u8054\u7f51\u836f\u54c1\u4fe1\u606f\u670d\u52a1\u8d44\u683c\u8bc1\u4e66\uff1a(\u6caa)-\u7ecf\u8425\u6027-2023-0144", "link": "//fe-video-qc.xhscdn.com/fe-platform/f37a08cacc088061beb38329c387c32fc48fc6fe.pdf", "title": "\u5c0f\u7ea2\u4e66_\u4e92\u8054\u7f51\u836f\u54c1\u4fe1\u606f\u670d\u52a1"}, {"label": "\u8fdd\u6cd5\u4e0d\u826f\u4fe1\u606f\u4e3e\u62a5\u7535\u8bdd\uff1a(021)5064 0584", "link": "//www.shjbzx.cn", "title": "\u5c0f\u7ea2\u4e66_\u4e0a\u6d77\u5e02\u4e92\u8054\u7f51\u4e3e\u62a5\u4e2d\u5fc3"}, {"label": "\u4e0a\u6d77\u5e02\u4e92\u8054\u7f51\u4e3e\u62a5\u4e2d\u5fc3", "link": "//www.shjbzx.cn", "title": "\u5c0f\u7ea2\u4e66_\u4e0a\u6d77\u5e02\u4e92\u8054\u7f51\u4e3e\u62a5\u4e2d\u5fc3"}, {"label": "\u7f51\u4e0a\u6709\u5bb3\u4fe1\u606f\u4e3e\u62a5\u4e13\u533a", "link": "//www.12377.cn", "title": "\u7f51\u4e0a\u6709\u5bb3\u4fe1\u606f\u4e3e\u62a5\u4e13\u533a"}, {"label": "\u81ea\u8425\u7ecf\u8425\u8005\u4fe1\u606f", "link": "//dc.xhscdn.com/06c2adb0-b353-11e9-9d0c-7be9ff8961c1/\u81ea\u8425\u7ecf\u8425\u8005\u4fe1\u606f\u516c\u793a.pdf", "title": "\u5c0f\u7ea2\u4e66_\u6caa\u516c\u7f51\u5b89\u5907"}, {"label": "\u7f51\u7edc\u6587\u5316\u7ecf\u8425\u8bb8\u53ef\u8bc1\uff1a\u6caa\u7f51\u6587(2024)1344-086\u53f7", "link": "//fe-video-qc.xhscdn.com/fe-platform/7970f6e8b70aedc995ba273d04b6b6751abcd63c.pdf", "title": "\u5c0f\u7ea2\u4e66_\u7f51\u7edc\u6587\u5316\u7ecf\u8425\u8bb8\u53ef"}, {"label": "\u4e2a\u6027\u5316\u63a8\u8350\u7b97\u6cd5 \u7f51\u4fe1\u7b97\u5907310101216601302230019\u53f7", "link": "https://beian.cac.gov.cn/api/static/fileUpload/principalOrithm/additional/user_c015445c-80ac-45f7-94d7-3871e961b1fe_d4425f3b-7f35-45af-b8d4-badd4424d6d5.pdf"}], "disableBanAlert": "false"}, "supportWebp": false, "serverTime": 1747126497266, "grayMode": false, "referer": "", "pwaAddDesktopPrompt": "undefined", "firstVisitUrl": "undefined", "easyAccessModalVisible": {"addDesktopGuide": false, "collectGuide": false, "keyboardList": false, "miniWindowGuide": false}, "currentLayout": "default", "fullscreenLocking": false, "feedbackPopupVisible": false, "trackFps": false, "supportAVIF": false, "imgFormatCollect": {"ssr": ["jpg"], "csr": ["jpg"]}, "isUndertake": false}, "user": {"loggedIn": true, "activated": false, "userInfo": {"gender": 2, "images": "https://sns-avatar-qc.xhscdn.com/avatar/645b7f8f2a34639eb26eb1cd.jpg?imageView2/2/w/360/format/webp", "imageb": "https://sns-avatar-qc.xhscdn.com/avatar/645b7f8f2a34639eb26eb1cd.jpg?imageView2/2/w/540/format/webp", "guest": false, "red_id": "11671269902", "user_id": "665d3aa30000000007006f25", "nickname": "11", "desc": "\u8fd8\u6ca1\u6709\u7b80\u4ecb", "userId": "665d3aa30000000007006f25", "redId": "11671269902"}, "follow": [], "userPageData": {}, "activeTab": {"key": 0, "index": 0, "query": "note", "label": "\u7b14\u8bb0", "lock": false, "subTabs": null, "feedType": 0}, "notes": [[], [], [], []], "isFetchingNotes": [false, false, false, false], "tabScrollTop": [0, 0, 0, 0], "userFetchingStatus": "undefined", "userNoteFetchingStatus": ["", "", "", ""], "bannedInfo": {"userId": "", "serverBanned": false, "code": 0, "showAlert": false, "reason": "", "api": ""}, "firstFetchNote": true, "noteQueries": [{"num": 30, "cursor": "", "userId": "", "hasMore": true, "page": 1}, {"num": 30, "cursor": "", "userId": "", "hasMore": true, "page": 1}, {"num": 30, "cursor": "", "userId": "", "hasMore": true, "page": 1}, {"num": 30, "cursor": "", "userId": "", "hasMore": true, "page": 1}], "pageScrolled": 0, "activeSubTab": "undefined", "isOwnBoard": true}, "board": {"boardListData": {}, "isLoadingBoardList": false, "boardDetails": {}, "boardFeedsMap": {}, "boardPageStatus": "pending", "userBoardList": []}, "login": {"loginMethod": "undefined", "from": "", "showLogin": false, "agreed": false, "showTooltip": false, "loginData": {"phone": "", "authCode": ""}, "errors": {"phone": "", "authCode": ""}, "qrData": {"backend": {"qrId": "", "code": ""}, "image": "", "status": "un_scanned"}, "counter": "undefined", "inAntiSpamChecking": false, "recentFrom": "", "isObPagesVisible": false, "obPageFillInProgress": null, "verificationCodeStartTime": 0, "ageSelectValue": "21", "hobbySelectValue": [], "genderSelectValue": "undefined", "inSpamCheckSendAuthCode": false, "isRegFusing": false, "loginStep": 0, "isLogining": false, "loginPadMountedTime": 0, "loginTips": "\u767b\u5f55\u540e\u63a8\u8350\u66f4\u61c2\u4f60\u7684\u7b14\u8bb0", "isRiskUser": false, "closeLoginModal": false, "traceId": "", "inAntiSpamCheckLogin": false}, "feed": {"query": {"cursorScore": "", "num": 30, "refreshType": 1, "noteIndex": 0, "unreadBeginNoteId": "", "unreadEndNoteId": "", "unreadNoteCount": 0, "category": "homefeed_recommend", "searchKey": "", "needNum": 20, "imageFormats": [], "needFilterImage": false}, "isFetching": false, "isError": false, "feedsWrapper": "undefined", "undertakeNote": "undefined", "feeds": [], "currentChannel": "homefeed_recommend", "unreadInfo": {"cachedFeeds": [], "unreadBeginNoteId": "", "unreadEndNoteId": "", "unreadNoteCount": 0, "timestamp": 0}, "validIds": {"noteIds": []}, "mfStatistics": {"timestamp": 0, "visitTimes": 0, "readFeedCount": 0}, "channels": "undefined", "isResourceDisplay": false, "isActivityEnd": false, "cancelFeedRequest": false, "prefetchId": "undefined", "mfRequestMetaData": {"start": null, "lasting": null}, "placeholderFeeds": [], "feedsCacheLogInfo": {"flag": "unknown", "errorCode": 0, "isHitMfCache": false, "SSRDocumentChecked": false, "SSRDocumentCheckedSuccess": false}, "isUsingPlaceholderFeeds": false, "placeholderFeedsConsumed": false, "isReplace": false, "isFirstSuccessFetched": false, "imgNoteFilterStatus": "unchecked", "ssrRequestStatus": 5, "ssrRenderExtra": ""}, "layout": {"layoutInfoReady": false, "columns": 6, "columnsWithSidebar": 6, "gap": {"vertical": 12, "horizontal": 24}, "columnWidth": 0, "interactionWidth": 0, "widthType": "normal", "bufferRow": 3}, "search": {"state": "auto", "searchContext": {"keyword": "", "page": 1, "pageSize": 20, "searchId": "", "sort": "general", "noteType": 0, "extFlags": [], "filters": [], "geo": ""}, "feeds": [], "searchValue": "", "suggestions": [], "userInputSugTrigger": "", "keywordFrom": 2, "tagSearch": [], "activeTagSearch": null, "searchFeedsWrapper": "undefined", "currentSearchType": "all", "hintWord": {"title": "\u641c\u7d22\u5c0f\u7ea2\u4e66", "searchWord": "\u5c0f\u7ea2\u4e66\u7f51\u9875\u7248", "hintWordRequestId": "default", "type": "default"}, "sugType": null, "queryTrendingInfo": "undefined", "queryTrendingParams": {"source": "ExploreNote", "searchType": "trend", "lastQuery": "", "lastQueryTime": 0, "wordRequestSituation": "FIRST_ENTER", "hintWord": "", "hintWordType": "", "hintWordRequestId": ""}, "queryTrendingFetched": false, "oneboxInfo": {}, "hasMore": true, "firstEnterSearchPage": true, "userLists": [], "fetchUserListsStatus": "auto", "isFetchingUserLists": false, "hasMoreUser": true, "searchCplId": "undefined", "wordRequestId": "undefined", "historyList": [], "searchPageHasPrevRoute": false, "searchHotSpots": [], "hotspotQueryNoteStep": "display", "hotspotQueryNoteIndex": 0, "canShowHotspotQueryNote": true, "forceHotspotSearch": false, "searchCardHotSpots": [], "isHotspotSearch": false, "filters": "undefined", "activeFilters": [], "filterParams": "undefined", "sessionId": "", "rootSearchId": "", "searchUserContext": {"keyword": "", "searchId": "", "page": 1, "pageSize": 15, "bizType": "web_search_user", "requestId": ""}}, "activity": {"isOpen": false, "currentUrl": "", "entryList": []}, "note": {"prevRouteData": {}, "prevRoute": "Empty", "commentTarget": {}, "isImgFullscreen": false, "gotoPage": "", "firstNoteId": "6804c3c3000000001c0352dd", "autoOpenNote": false, "topCommentId": "", "noteDetailMap": {"6804c3c3000000001c0352dd": {"comments": {"list": [], "cursor": "", "hasMore": true, "loading": false, "firstRequestFinish": false}, "currentTime": 1747126497306, "note": {"xsecToken": "ABnas8F8abYV8JVHsJtqGXK4XXB10g0J1_oJsNxdxfeDI=", "desc": "#\u6a58\u732b[\u8bdd\u9898]# #\u5438\u732b[\u8bdd\u9898]# #\u6211\u5bb6\u5ba0\u7269\u597d\u53ef\u7231[\u8bdd\u9898]# #\u6211\u7684\u5b9d\u8d1d[\u8bdd\u9898]# #\u5c0f\u7ea2\u4e66\u517b\u5ba0\u5021\u8bae[\u8bdd\u9898]# #\u5939\u5b50\u732b[\u8bdd\u9898]# #\u5ba0\u7269\u5b85\u5bb6\u6587\u827a\u590d\u5174[\u8bdd\u9898]#", "user": {"userId": "5d32ea9900000000100106f3", "nickname": "\u591a\u591a\u53c8\u80d6\u4e86", "avatar": "https://sns-avatar-qc.xhscdn.com/avatar/64733e599bede08712d6ec7f.jpg", "xsecToken": "AB1RBwbWA-Vc-G9wU1K9b2WNBEeLtGaEXofgig3Mf1wro="}, "video": {"media": {"video": {"bizName": 110, "bizId": "281480215554904797", "duration": 13, "md5": "b469c3a4257c7e48cec5da43b1374b29", "hdrType": 0, "drmType": 0, "streamTypes": [259, 114]}, "stream": {"h266": [], "av1": [], "h264": [{"duration": 12000, "videoBitrate": 906642, "ssim": 0, "size": 1468221, "vmaf": -1, "streamType": 259, "format": "mp4", "fps": 30, "audioCodec": "aac", "qualityType": "HD", "height": 1282, "avgBitrate": 978814, "rotate": 0, "hdrType": 0, "backupUrls": ["http://sns-bak-v6.xhscdn.com/stream/79/110/259/01e804c2f7088b370103700396529cedc7_259.mp4"], "videoCodec": "h264", "psnr": 0, "streamDesc": "WM_X264_MP4", "defaultStream": 0, "volume": 0, "audioChannels": 2, "masterUrl": "http://sns-video-qc.xhscdn.com/stream/79/110/259/01e804c2f7088b370103700396529cedc7_259.mp4?sign=343b2c54185c62a17f4bfbe3a156e70c&t=6827a621", "weight": 62, "width": 720, "videoDuration": 12000, "audioBitrate": 64833, "audioDuration": 11965}], "h265": [{"streamDesc": "X265_MP4_WEB_114", "duration": 12000, "videoDuration": 12000, "audioCodec": "aac", "audioDuration": 11980, "psnr": 42.81100082397461, "videoBitrate": 959836, "videoCodec": "hevc", "size": 1645200, "volume": 0, "rotate": 0, "masterUrl": "http://sns-video-qc.xhscdn.com/stream/79/110/114/01e804c2f7088b374f03700196529d2073_114.mp4?sign=22254340fb9b46b16f31002e93202e84&t=6827a621", "fps": 30, "backupUrls": ["http://sns-bak-v6.xhscdn.com/stream/79/110/114/01e804c2f7088b374f03700196529d2073_114.mp4"], "weight": 62, "qualityType": "HD", "audioBitrate": 129504, "hdrType": 0, "ssim": 0, "vmaf": -1, "audioChannels": 2, "streamType": 114, "width": 720, "height": 1282, "avgBitrate": 1096800, "defaultStream": 0, "format": "mp4"}]}, "videoId": 137365024049498930}, "image": {"firstFrameFileid": "110/0/01e804c2f7088b3700100000000196529cbd82_0.jpg", "thumbnailFileid": "110/0/01e804c2f7088b3700100000000196529cc596_0.webp"}, "capa": {"duration": 12}, "consumer": {"originVideoKey": "pre_post/1040g2t031ggb19qgj8005n9itack21nj1hbhlv8"}}, "tagList": [{"name": "\u6a58\u732b", "type": "topic", "id": "5bec5e73aafb3e0001aca92a"}, {"id": "5950bde0cd30d856de734427", "name": "\u5438\u732b", "type": "topic"}, {"id": "58f7213df5a263759091def0", "name": "\u6211\u5bb6\u5ba0\u7269\u597d\u53ef\u7231", "type": "topic"}, {"name": "\u6211\u7684\u5b9d\u8d1d", "type": "topic", "id": "543d3a58d6e4a977fef0ae02"}, {"id": "674eb606000000000b005830", "name": "\u5c0f\u7ea2\u4e66\u517b\u5ba0\u5021\u8bae", "type": "topic"}, {"id": "613f1df50000000001002cfc", "name": "\u5939\u5b50\u732b", "type": "topic"}, {"id": "67dab0820000000013010dee", "name": "\u5ba0\u7269\u5b85\u5bb6\u6587\u827a\u590d\u5174", "type": "topic"}], "shareInfo": {"unShare": false}, "noteId": "6804c3c3000000001c0352dd", "title": "\u6c14\u9f13\u9f13\u7684\u5999\u54c7\u54aa\u5b50", "interactInfo": {"likedCount": "7.9\u4e07", "collected": false, "collectedCount": "5138", "commentCount": "1254", "shareCount": "6682", "followed": false, "relation": "none", "liked": false}, "lastUpdateTime": 1745142724000, "ipLocation": "\u91cd\u5e86", "imageList": [{"traceId": "", "urlDefault": "http://sns-webpic-qc.xhscdn.com/202505131654/861cab2d9283721808eac07c827bccc8/1040g2sg31ggb4h3pja005n9itack21nja8j7v80!nd_dft_wlteh_jpg_3", "infoList": [{"url": "http://sns-webpic-qc.xhscdn.com/202505131654/9c19ae1a8167b7eb596b0889b69f02cb/1040g2sg31ggb4h3pja005n9itack21nja8j7v80!nd_prv_wlteh_jpg_3", "imageScene": "WB_PRV"}, {"imageScene": "WB_DFT", "url": "http://sns-webpic-qc.xhscdn.com/202505131654/861cab2d9283721808eac07c827bccc8/1040g2sg31ggb4h3pja005n9itack21nja8j7v80!nd_dft_wlteh_jpg_3"}], "urlPre": "http://sns-webpic-qc.xhscdn.com/202505131654/9c19ae1a8167b7eb596b0889b69f02cb/1040g2sg31ggb4h3pja005n9itack21nja8j7v80!nd_prv_wlteh_jpg_3", "stream": {}, "livePhoto": false, "fileId": "", "height": 1440, "width": 1080, "url": ""}], "type": "video", "atUserList": [], "time": 1745142723000}}}, "serverRequestInfo": {"state": "success", "errorCode": 0, "errMsg": ""}, "volume": 0, "recommendVideoMap": {}, "videoFeedType": "note_source", "rate": 1, "currentNoteId": "6804c3c3000000001c0352dd", "forceScrollToComment": false, "mediaWidth": 450, "noteHeight": 800}, "nioStore": {"collectionListDataSource": "undefined", "error": "undefined"}, "notification": {"isFetching": false, "activeTabKey": -1, "notificationCount": {"unreadCount": 0, "mentions": 0, "likes": 0, "connections": 0}, "notificationMap": {"mentions": {"messageList": [], "hasMore": true, "cursor": ""}, "likes": {"messageList": [], "hasMore": true, "cursor": ""}, "connections": {"messageList": [], "hasMore": true, "cursor": ""}}}, "redMoji": {"mojiData": {"version": "", "redmojiTabs": [], "redmojiMap": {}}}}
        # 获取单一视频笔记信息
        # url = "https://www.xiaohongshu.com/explore/6804c3c3000000001c0352dd?xsec_token=ABnas8F8abYV8JVHsJtqGXK4XXB10g0J1_oJsNxdxfeDI=&xsec_source=pc_feed"
        # result = await self.fetch_one_video(url)
        # print(result)

        # 获取单一图文笔记信息
        # url = "https://www.xiaohongshu.com/explore/680b87f9000000000f03a497?xsec_token=ABIX--M-eqnHdnkohztWwEyIfFtE4YT3CUdTjCD82dK60=&xsec_source=pc_feed"
        # result = await self.fetch_one_note(url)
        # print(result)

        # 获取一个作品的一级评论信息
        note_id = "680b87f9000000000f03a497"
        x_sec_token = "ABGKRE1TQqLF8Txl4rcSOTWfVmTOimU7qra5R4sZrvOVc=" # 随便获取一个就行,无论哪个用户哪个接口哪个界面的
        result = await self.fetch_first_level_comment(note_id, x_sec_token)
        print(result)
if __name__ == "__main__":
    crawler = XhsWebCrawler()
    # 开始时间
    start = time.time()
    asyncio.run(crawler.main())
    end = time.time()
    print(f"耗时：{end - start}")