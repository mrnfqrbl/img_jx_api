import json
import os
from io import BytesIO
from typing import Any, Dict, List, Optional, Union

import piexif
from PIL import Image
from PIL.PngImagePlugin import PngImageFile


class ImageMetadataExtractor:

    @staticmethod
    def _load_image(input_data: Union[str, bytes, BytesIO]) -> Optional[Image.Image]:
        """
        加载图像数据，支持文件路径、二进制流或 BytesIO。

        参数:
            input_data (Union[str, bytes, BytesIO]): 图像数据，可以是文件路径（str），
                                                      图像的二进制数据（bytes）或 BytesIO 对象。

        返回:
            Image.Image 或 None: 返回 PIL 图像对象，如果加载失败，返回 None。
        """
        try:
            # 如果是文件路径
            if isinstance(input_data, str):
                image = Image.open(input_data)
            # 如果是字节数据或 BytesIO 对象
            elif isinstance(input_data, (bytes, BytesIO)):
                image = Image.open(BytesIO(input_data) if isinstance(input_data, bytes) else input_data)
            else:
                raise ValueError("输入的数据类型不支持，必须是文件路径、字节数据或 BytesIO 对象。")

            # 检查图像格式
            if image.format is None:
                raise ValueError("无法识别图像格式")

            return image

        except Exception as e:
            # 返回具体的错误信息
            return f"加载图像失败: {str(e)}"

    @staticmethod
    def extract_exif(input_data: Union[str, bytes]) -> Optional[Dict[str, Any]]:
        """提取 EXIF 数据，支持文件路径或二进制流"""
        image = ImageMetadataExtractor._load_image(input_data)
        if image and 'exif' in image.info:
            try:
                return piexif.load(image.info['exif'])
            except Exception as e:
                print(f"提取 EXIF 数据失败: {e}")
        return None

    @staticmethod
    @staticmethod
    def extract_png_metadata(input_data: Union[str, bytes]) -> Dict[str, str]:
        """从 PNG 图像中提取元数据（tEXt 或 iTXt），支持文件路径或二进制流"""
        # 加载图像
        image = ImageMetadataExtractor._load_image(input_data)

        # 如果图像是 PNG 格式
        if isinstance(image, PngImageFile):
            text_chunks = image.text
            metadata = {}

            # 将所有元数据填充到字典中
            for keyword, value in text_chunks.items():
                metadata[keyword] = value  # keyword 为键，value 为值

            return metadata

        # 如果不是 PNG 格式，返回空字典
        return {}

    @staticmethod
    def get_file_info(input_data: Union[str, bytes]) -> Dict[str, Any]:
        """获取文件的基本信息，支持文件路径或二进制流"""
        image = ImageMetadataExtractor._load_image(input_data)
        if image:
            return {
                "filename": input_data if isinstance(input_data, str) else "in-memory-image",
                "filesize": ImageMetadataExtractor.get_file_size(input_data),
                "image_width": image.width,
                "image_height": image.height,
                "format": image.format
            }
        return {}

    @staticmethod
    def get_file_size(input_data: Union[str, bytes]) -> str:
        """获取文件大小，支持文件路径或二进制流"""
        # 如果是文件路径
        if isinstance(input_data, str):
            try:
                file_size = os.path.getsize(input_data)
                return f"{round(file_size / (1024 ** 2), 2)} MB"
            except Exception as e:
                print(f"获取文件大小失败: {e}")
                return "0 MB"

        # 如果是二进制流，获取流的大小
        elif isinstance(input_data, bytes):
            return f"{round(len(input_data) / (1024 ** 2), 2)} MB"

        return "0 MB"

    @staticmethod
    def parse_comment(comment_text: str) -> Dict[str, Any]:
        """解析 Comment 字段中的 JSON 数据"""
        try:
            # 解析 Comment 字段中的 JSON 数据
            return json.loads(comment_text)
        except json.JSONDecodeError as e:
            print(f"Comment 字段 JSON 解码失败: {e}")
            return {}

    @staticmethod
    def get_all_metadata(input_data: Union[str, bytes]) -> Dict[str, Any]:
        """获取所有的元数据，包括 EXIF 和 Stable Diffusion 信息，支持文件路径或二进制流"""
        metadata = {
            "file_info": ImageMetadataExtractor.get_file_info(input_data),
            "exif": ImageMetadataExtractor.extract_exif(input_data),
            "stable_diffusion_metadata": ImageMetadataExtractor.extract_png_metadata(input_data)
        }
        #print(f"原始sdm：{ImageMetadataExtractor.extract_png_metadata(input_data)}")

        if 'stable_diffusion_metadata' in metadata and isinstance(metadata['stable_diffusion_metadata'], dict):
            # 遍历 stable_diffusion_metadata 字典
            for keyword, entry in metadata['stable_diffusion_metadata'].items():
                if keyword == "Comment":
                    # 解析 Comment 字段为 JSON 格式的字典
                    entry = ImageMetadataExtractor.parse_comment(entry)
                    metadata['stable_diffusion_metadata'][keyword] = entry

        # 如果没有 EXIF 信息或不需要处理 EXIF，删除该键
        if not ImageMetadataExtractor.extract_exif(input_data):
            if 'exif' in metadata:
                del metadata['exif']

        return metadata


class MainCoordinator:
    @staticmethod
    def handle_input(input_data: Union[str, bytes]) -> Dict[str, Any]:
        """主协调器，处理输入数据并协调元数据提取操作"""
        # 调用 ImageMetadataExtractor 的方法来获取所有元数据
        metadata = ImageMetadataExtractor.get_all_metadata(input_data)

        # 如果需要，可以在这里做进一步的处理，例如格式化或转换
        return metadata


if __name__ == "__main__":
#     file_path = r"D:\xm\img-jx\input\3.png"
#
# # 读取图片文件为字节流
#     with open(file_path, "rb") as f:
#         img_data = f.read()  # 读取为字节流
#
# # 传递字节流给 handle_input 函数
#     metadata = MainCoordinator.handle_input(img_data)
#
# # 输出处理后的元数据
#     print(json.dumps(metadata, indent=4, ensure_ascii=False))
    file_path = r"D:\xm\img-jx\input\3.png"

# 读取图片文件为字节流
    with open(file_path, "rb") as f:
        img_data = BytesIO(f.read())  # 将读取的字节流封装到 BytesIO 对象中

# 传递字节流给 handle_input 函数
    metadata = ImageMetadataExtractor.get_all_metadata(img_data)

# 输出处理后的元数据
    print(json.dumps(metadata, indent=4, ensure_ascii=False))


