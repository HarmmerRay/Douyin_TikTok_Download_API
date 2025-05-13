from urllib.request import Request

from fastapi import APIRouter, Query, Request, HTTPException

from app.api.models.APIResponseModel import ResponseModel, ErrorResponseModel
from crawlers.xhs.web.web_crawler import XhsWebCrawler

router = APIRouter()
# 获取单个作品数据
@router.get("/fetch_one_video", response_model=ResponseModel, summary="获取单个视频作品数据/Get single video data")
async def fetch_one_video(request: Request,
                          video_id: str = Query(example="6809acdd000000001202c014", description="作品id/Video id")):
    try:
        data = await XhsWebCrawler.fetch_one_video(video_id)
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