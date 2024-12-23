from typing import Optional
from xml.sax.handler import property_interning_dict

from fastapi import APIRouter, UploadFile


from app.api_server.route_img_jx import image_jx,img_jx_and_db

router = APIRouter()

# GET 请求：可以接收 URL 或文件上传的图片进行处理
@router.get("/api/img_jx")
async def process_image_request(
        url: Optional[str] = None,  # 可选的 URL 查询参数
        file: Optional[UploadFile] = None  # 可选的上传文件
):
    return await image_jx(url, file)
@router.post("/api/img_jx_and_db")
async def api_img_jx_and_db(
        url: Optional[str] = None,  # 可选的 URL 查询参数
        file: Optional[UploadFile] = None  # 可选的上传文件
):
    return await img_jx_and_db(url, file)


# POST 请求：接收数据（在这里我们只是作为占位符，未实现）
@router.post("/api/img_rjx")
async def receive_data():
    return {"message": "未实现"}
# 添加心跳请求
@router.get("/api/health")
async def health_check():
    return {"status": "OK", "message": "服务正常运行"}