from urllib.request import Request

from fastapi import APIRouter, Query, Request, HTTPException

from app.api.models.APIResponseModel import ResponseModel, ErrorResponseModel
from crawlers.xhs.web.web_crawler import XhsWebCrawler

router = APIRouter()
XhsWebCrawler = XhsWebCrawler()
# 获取单个视频作品数据
@router.get("/fetch_one_video", response_model=ResponseModel, summary="获取单个视频作品数据/Get single video data")
async def fetch_one_video(request: Request,
                          url: str = Query(example="https://www.xiaohongshu.com/explore/6804c3c3000000001c0352dd?xsec_token=ABnas8F8abYV8JVHsJtqGXK4XXB10g0J1_oJsNxdxfeDI=&xsec_source=pc_feed", description="作品url地址/Work URL")):
    try:
        print(url)
        data = await XhsWebCrawler.fetch_one_video(url)
        return ResponseModel(code=200,
                             router=request.url.path,
                             data=data)
    except Exception as e:
        status_code = 400
        detail = ErrorResponseModel(code=status_code,
                                    router=request.url.path,
                                    params=dict(request.query_params),
                                    )
        raise HTTPException(status_code=status_code, detail=detail.dict())

# 获取单个图文作品数据
@router.get("/fetch_one_note", response_model=ResponseModel, summary="获取单个图文作品数据/Get single note(pic) data")
async def fetch_one_note(request: Request,
                          url: str = Query(example="https://www.xiaohongshu.com/explore/680b87f9000000000f03a497?xsec_token=ABIX--M-eqnHdnkohztWwEyIfFtE4YT3CUdTjCD82dK60=&xsec_source=pc_feed", description="作品url地址/Work URL")):
    try:
        print(url)
        data = await XhsWebCrawler.fetch_one_note(url)
        return ResponseModel(code=200,
                             router=request.url.path,
                             data=data)
    except Exception as e:
        status_code = 400
        detail = ErrorResponseModel(code=status_code,
                                    router=request.url.path,
                                    params=dict(request.query_params),
                                    )
        raise HTTPException(status_code=status_code, detail=detail.dict())

# 获取作品的一级评论数据
@router.get("/fetch_first_level_comments", response_model=ResponseModel, summary="获取作品一级评论数据/Get first level comments")
async def fetch_first_level_comments(request: Request,
                                     note_id: str = Query(example="680b87f9000000000f03a497", description="作品ID/Work ID"),
                                     xsec_toekn: str =Query(example="ABGKRE1TQqLF8Txl4rcSOTWfVmTOimU7qra5R4sZrvOVc=", description="任意一个xsec_token即可，打开小红书网站在网址框内查看/Xsec_token") ):
    try:
        data = await XhsWebCrawler.fetch_first_level_comment(note_id,xsec_toekn)
        return ResponseModel(code=200,
                             router=request.url.path,
                             data=data)
    except Exception as e:
        status_code = 400
        detail = ErrorResponseModel(code=status_code,
                                    router=request.url.path,
                                    params=dict(request.query_params),
                                    )
        raise HTTPException(status_code=status_code, detail=detail.dict())