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