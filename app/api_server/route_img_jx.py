import ssl
from typing import Optional

from fastapi import HTTPException, UploadFile
from io import BytesIO
import httpx  # 使用 httpx 进行异步 HTTP 请求
from app.api_server.img_jx import img_metadata, save_db


# 处理 URL 获取图片并转换为 io.BytesIO 流
async def fetch_image_from_url(url: str) -> BytesIO:
    try:
        # 创建自定义 SSLContext
        context = ssl.create_default_context()
        context.options |= ssl.OP_NO_SSLv2  # 禁用 SSLv2
        context.options |= ssl.OP_NO_SSLv3  # 禁用 SSLv3
        context.set_ciphers('TLS_AES_128_GCM_SHA256:TLSv1.2')  # 强制使用 TLSv1.2 作为兼容选项

        # 使用自定义的 SSLContext 进行请求
        async with httpx.AsyncClient(verify=context) as client:  # 传递 SSLContext
            response = await client.get(url)
            response.raise_for_status()  # 如果请求失败，抛出异常
            # print("HTTP 响应类型:",type(response.content) )

            # 将图片内容转为 BytesIO 流
            img_data = BytesIO(response.content)
            return img_data
    except httpx.RequestError as e:
        # 捕获 httpx 请求错误
        raise HTTPException(status_code=400, detail=f"无法从 URL 获取图片: {str(e)}")
    except Exception as e:
        # 捕获其他异常
        raise HTTPException(status_code=400, detail=f"图片处理失败: {str(e)}")

# 处理上传的图片文件并转换为 io.BytesIO 流
async def process_uploaded_image(file: UploadFile) -> BytesIO:
    try:
        img_data = BytesIO(await file.read())  # 将上传的图片转为 BytesIO 流
        return img_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"上传图片处理失败: {str(e)}")


async def image_jx(
        url: Optional[str] = None,  # 可选的 URL 查询参数
        file: Optional[UploadFile] = None  # 可选的上传文件
):
    if url:
        # 如果提供了 URL，尝试获取该 URL 的图片
        image_data = await fetch_image_from_url(url)
        img_metadata_url=await img_metadata(image_data)
        return {f"状态：成功,返回：{img_metadata_url}"}
    elif file:
    # 如果提供了文件，处理上传的图片
        image_data = await process_uploaded_image(file)
        img_metadata_file=await img_metadata(image_data)
        return {f"状态：成功,返回：{img_metadata_file}"}
    else:
        raise HTTPException(status_code=400, detail="必须提供图片 URL 或 上传图片文件")




async def img_jx_and_db(
        url: Optional[str] = None,  # 可选的 URL 查询参数
        file: Optional[UploadFile] = None  # 可选的上传文件
):
    if url:
        # 如果提供了 URL，尝试获取该 URL 的图片
        # print(url)
        image_data = await fetch_image_from_url(url)
        返回=await save_db(image_data)
        return {f"状态：成功,返回：{返回}"}
    elif file:
        # 如果提供了文件，处理上传的图片
        image_data = await process_uploaded_image(file)
        返回=await save_db(image_data)
        return {f"状态：成功,返回：{返回}"}



