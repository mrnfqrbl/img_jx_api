import os
from io import BytesIO
from typing import Optional
import json

from app.utils.en_cn import MetadataTranslator
from app.core.rs import Reading_Steganography
from app.core.ripd import ImageMetadataExtractor
from app.db.db import collection
# 图片元数据处理逻辑
UPLOAD_FOLDER = "E:\\ai\\jx"
async def img_metadata(img_data: BytesIO):
    # 获取所有元数据
    exif = ImageMetadataExtractor.get_all_metadata(img_data)
    # print("exif:",exif)

    # 检查是否有 Comment 字段，如果有则直接返回 exif
    if 'stable_diffusion_metadata' in exif:
    # 如果 'stable_diffusion_metadata' 存在，则继续检查是否有 Comment
        if 'Comment' in exif and exif['Comment']:  # 检查 Comment 是否存在且非空
            exif_cn = MetadataTranslator.translate_to_chinese(exif)
        # print("exif_cn:",exif_cn)
            return exif_cn  # 如果有 Comment 字段，直接返回 exif

    # 如果没有 Comment 字段，调用隐写分析逻辑
    rs = Reading_Steganography.main(img_data)
    # 使用json.loads()将Comment字段中的字符串解析为字典
    comment_data = json.loads(rs['Comment'])

# 更新rs字典中的Comment字段
    rs['Comment'] = comment_data
    print(type(rs['Comment']))




# 翻译元数据到中文
    exif_cn = MetadataTranslator.translate_to_chinese(exif)
    rs_cn = MetadataTranslator.translate_to_chinese(rs)
    #print("rscntype:",type(rs_cn))
    scxx=rs_cn.get('生成信息')
    #print("scxxtype",type(scxx))

    # print("rscn:",rs_cn)
    # print("exif_cn:",exif_cn)
    # 合并元数据和隐写信息，去重时优先保留 exif 中的数据

    img_metadata = {}

    # 合并 exif_cn 和 rs_cn，遵循合并规则
    for key, value in exif_cn.items():
        if key == "稳定扩散(stable_diffusion)或novelai元数据":
            # 如果 exif_cn 中存在 '稳定扩散(stable_diffusion)或novelai元数据' 键
            # 则直接将 rs_cn 的内容添加到这个字段
            img_metadata[key] = {**value, **rs_cn}
        else:
            img_metadata[key] = value

    # 将 rs_cn 中没有在 exif_cn 中的项添加到最终结果中
    for key, value in rs_cn.items():
        if key not in img_metadata:
            img_metadata[key] = value

    # print("img_metadata:", img_metadata)
    # sd= img_metadata.get('稳定扩散(stable_diffusion)或novelai元数据')
    # print("sdddddddddddddddddddddd",type(sd))
    return img_metadata



async def save_db(img_data: BytesIO) -> Optional[str]:
    # 提取 tags（实际中应该用你已有的 img_metadata 函数）
    tags = await img_metadata(img_data)  # 假设传入的 tag 已经是提取过的
    #print(type(tags))
    #print("img_metadata:", tags)
    # 获取嵌套的 "生成信息" 部分
    generation_info = tags.get("稳定扩散(stable_diffusion)或novelai元数据", {}).get("生成信息", {})
    print(type(generation_info))
    print("生成信息：",generation_info)

    # 要求的字段
    required_fields = ["提示词", "步数", "缩放", "采样器", "SM", "SM动态", "宽度", "高度", "负面"]

    # 创建一个新字典，只包括那些非空且符合要求的字段
    tag_document = {}

    # 从生成信息中提取字段
    for field in required_fields:
        value = generation_info.get(field)
        if value is not None:  # 只取非None值，布尔值会被视作有效值
            tag_document[field] = value

    # 如果 tag_document 为空，则返回提取为空
    if not tag_document:
        return f"提取为空,提取前为：{tags}"

    # 获取数据库中下一个图片文件名（通过序号）
    last_image = await collection.find_one(sort=[("序号", -1)])  # 查找序号最大（最新的）文档
    next_index = 1 if not last_image else last_image.get("序号", 0) + 1

    # 图片保存路径
    file_name = f"{next_index}.png"  # 图片文件名按照序号生成
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    # 确保上传目录存在
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)  # 创建目录
    # 将图片数据保存为文件
    with open(file_path, 'wb') as f:
        f.write(img_data.getvalue())

    # 将 tag_document 和文件名存入数据库
    tag_document["文件名"] = file_name
    tag_document["序号"] = next_index

    # 存储元数据到数据库
    await collection.insert_one(tag_document)

    return f"文件保存成功，文件名：{file_name}"



