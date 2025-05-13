from fastapi import APIRouter, Body, Query, Request, HTTPException

from app.api.models.APIResponseModel import ResponseModel, ErrorResponseModel
from crawlers.ks.web.web_crawler import KsWebCrawler

router = APIRouter()

# 获取单个作品数据
@router.get("/fetch_user_profile", response_model=ResponseModel, summary="获取用户主页个人数据/Get user profile")
async def fetch_one_video(request: Request,
                          user_id: str = Query(example="6809acdd000000001202c014", description="用户id/user id")):
    try:
        data = await KsWebCrawler.fetch_user_profile(user_id=user_id)
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