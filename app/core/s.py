import gzip
import json
import io
from PIL import Image
from typing import Union


class Steganography:
    MAGIC_NUMBER = "stealth_pngcomp"

    class DataWriter:
        def __init__(self, data=None):
            """初始化时可以传入数据，若未传入则默认为空列表"""
            if data is None:
                self.data = []  # 初始化为空列表
            else:
                self.data = data
            self.index = 0

        def write_bit(self, bit):
            """写入一个位（bit）"""
            if self.index >= len(self.data):
                self.data.append(0)  # 扩展列表以适应新数据
            self.data[self.index] = bit
            self.index += 1

        def write_n_bits(self, bits):
            """写入 n 个位（bit）"""
            for bit in bits:
                self.write_bit(bit)

        def write_byte(self, byte):
            """写入一个字节（byte）"""
            for i in range(8):
                bit = (byte >> (7 - i)) & 1
                self.write_bit(bit)

        def write_n_bytes(self, bytes_):
            """写入 n 个字节（byte）"""
            for byte in bytes_:
                self.write_byte(byte)

        def write_int32(self, value):
            """写入一个 32 位整数（4 字节）"""
            self.write_n_bytes(value.to_bytes(4, byteorder='big'))

    @staticmethod
    def load_image(image_path: Union[str, io.BytesIO]) -> Image.Image:
        """加载图片，只打开一次"""
        if isinstance(image_path, str):
            img = Image.open(image_path).convert('RGBA')  # 如果是路径，直接打开
        elif isinstance(image_path, io.BytesIO):
            img = Image.open(image_path).convert('RGBA')  # 如果是文件对象，使用 BytesIO
        else:
            raise ValueError("image_path 必须是文件路径（str）或文件对象（BytesIO）")
        return img

    @staticmethod
    def embed_lsb(img: Image.Image, lsb_data: list):
        """将数据嵌入到图像的最低有效位（LSB）"""
        pixels = img.load()
        width, height = img.size
        total_pixels = width * height

        # 检查 lsb_data 是否足够填充图像的所有像素
        if len(lsb_data) < total_pixels:
            # 填充空字节（零）以确保数据长度与图像像素数匹配
            additional_bits_needed = total_pixels - len(lsb_data)
            lsb_data.extend([0] * additional_bits_needed)  # 用零填充到所需长度

        count = 0
        for x in range(width):  # 先按列遍历
            for y in range(height):  # 再按行遍历
                r, g, b, a = pixels[x, y]  # 提取 RGBA 值
                new_a = (a & ~1) | lsb_data[count]  # 设置新的 alpha 通道最低有效位
                pixels[x, y] = (r, g, b, new_a)  # 修改 alpha 通道
                count += 1

    @staticmethod
    def prepare_data(data: dict) -> list:
        """准备数据：压缩并编码为最低有效位（LSB）"""
        # 将数据转换为 JSON 格式
        json_data = json.dumps(data)

        # 使用 Gzip 压缩数据
        compressed_data = gzip.compress(json_data.encode('utf-8'))

        # 添加魔术数字和数据长度
        lsb_data = []
        magic_bytes = list(Steganography.MAGIC_NUMBER.encode('utf-8'))  # 魔术数字转换为字节

        # 创建数据
        data_length = len(compressed_data) * 8  # 数据长度按位计算

        # 将魔术数字、数据长度和压缩数据转换为最低有效位
        writer = Steganography.DataWriter(lsb_data)

        # 写入魔术数字、数据长度和压缩数据
        writer.write_n_bytes(magic_bytes)  # 写入魔术数字
        writer.write_int32(data_length)    # 写入数据长度
        writer.write_n_bytes(list(compressed_data))  # 写入压缩数据

        return lsb_data

    @staticmethod
    def embed_data_into_image(image_path: Union[str, io.BytesIO], data: dict) -> Image.Image:
        """将数据嵌入到图像中并返回修改后的图像"""
        img = Steganography.load_image(image_path)

        # 准备数据：压缩并转换为 LSB
        lsb_data = Steganography.prepare_data(data)

        # 将数据嵌入到图像中
        Steganography.embed_lsb(img, lsb_data)

        return img

    @staticmethod
    def save_image(img: Image.Image, output_path: str):
        """保存修改后的图像"""
        img.save(output_path)

    @staticmethod
    def main(image_path: Union[str, io.BytesIO], data: dict, output_path: str):
        """主函数，执行数据嵌入和保存图像"""
        # 将数据嵌入图像
        modified_img = Steganography.embed_data_into_image(image_path, data)

        # 保存修改后的图像
        Steganography.save_image(modified_img, output_path)


if __name__ == "__main__":
    # 需要嵌入的数据
    data_to_embed = {
        "message": "卧槽卧槽!",          # 秘密消息
        "author": "Steganography",                      # 作者
        "timestamp": "2024-12-22T10:00:00Z",            # 时间戳，格式为ISO 8601
        "version": "1.0.0",                              # 数据版本
        "category": "Confidential",                      # 数据分类
        "encryption_key": "my_encryption_key_12345",    # 如果数据加密，可以嵌入加密密钥（当然最好是加密）
        "checksum": "abc123xyz456",                     # 用于验证数据完整性或防止篡改的校验和
        "file_hash": "d2d2d2a02d5a85baf0b20a6277a9b6cc", # 文件的哈希值（可以嵌入加密文件的哈希）
        "user_id": "user_00123",                        # 用户ID
        "access_level": "admin",                         # 权限级别
        "license": "GPLv3",                              # 使用的许可证类型
        "comments": "This image contains hidden metadata for testing purposes.",  # 备注
        "extra_info": {                                  # 其他扩展信息，可以是字典或复杂结构
            "sub_author": "John Doe",
            "project_name": "Steganography Project"
        },
        "tags": ["confidential", "test", "hidden"],      # 标签，用于描述该数据的特性
        "custom_field": "Some custom data here"          # 自定义字段
    }


    # 图片路径（文件路径或文件对象）
    #image_path = r"D:\xm\img-jx\output\3_with_metadata.png"  # 或者
    image_path = io.BytesIO(open(r"D:\xm\img-jx\output\3_with_metadata.png", "rb").read())  # 或者文件对象

    # 输出图片路径
    output_path = r"D:\xm\img-jx\output\modified_image.png"

    # 不需要实例化类，直接调用静态方法
    Steganography.main(image_path, data_to_embed, output_path)

    print(f"修改后的图像已保存到: {output_path}")
