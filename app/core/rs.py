import gzip
import json
import io
from PIL import Image
from typing import Union

class Reading_Steganography:
    MAGIC_NUMBER = "stealth_pngcomp"

    class DataReader:
        def __init__(self, data):
            # 传入的数据应该是一个字节序列或列表
            self.data = data
            self.index = 0

        def read_bit(self):
            """读取一个位（bit）"""
            bit = self.data[self.index]
            self.index += 1
            return bit

        def read_n_bits(self, n):
            """读取 n 个位（bit）"""
            bits = []
            for _ in range(n):
                bits.append(self.read_bit())
            return bits

        def read_byte(self):
            """读取一个字节（byte）"""
            byte = 0
            for i in range(8):
                byte |= self.read_bit() << (7 - i)
            return byte

        def read_n_bytes(self, n):
            """读取 n 个字节（byte）"""
            bytes_ = []
            for _ in range(n):
                bytes_.append(self.read_byte())
            return bytes_

        def read_int32(self):
            """读取一个 32 位整数（4 字节）"""
            bytes_ = self.read_n_bytes(4)
            # 将字节转换为 32 位整数，假设数据是大端存储
            return int.from_bytes(bytes_, byteorder='big')

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
    def extract_lsb(img: Image.Image) -> list:
        """提取图像中的最低有效位（LSB）"""
        pixels = img.load()

        # 获取图像尺寸
        width, height = img.size

        # 存储最低有效位（LSB）
        lsb_data = []

        # 提取像素的最低有效位，按列行顺序（0.0, 0.1, ..., 1.0, 1.1, ..., width-1.0, width-1.1, ...）
        for x in range(width):  # 先按列遍历
            for y in range(height):  # 再按行遍历
                r, g, b, a = pixels[x, y]  # 提取 RGBA 值
                lsb = a & 1  # 获取最低有效位
                lsb_data.append(lsb)  # 存储最低有效位
        return lsb_data

    @staticmethod
    def get_magic_string(lowest_data, magic: str) -> str:
        """获取图像中的魔术数字"""
        reader = Reading_Steganography.DataReader(lowest_data)
        read_magic = reader.read_n_bytes(len(magic))  # 读取与 magic 长度相同的字节数

        # 将字节转换为字符串
        magic_string = ''.join(chr(byte) for byte in read_magic)

        #print(f"读取到的魔术数字字节：{read_magic}")
        print(f"读取到的魔术数字: {magic_string}")
        return magic_string

    @staticmethod
    def extract_stealth_data(lowest_data) -> Union[dict, None]:
        """提取隐藏的有效数据"""
        reader = Reading_Steganography.DataReader(lowest_data)

        # 读取魔术数字
        magic = Reading_Steganography.MAGIC_NUMBER
        read_magic = reader.read_n_bytes(len(magic))
        magic_string = ''.join(chr(byte) for byte in read_magic)

        if magic == magic_string:
            data_length = reader.read_int32()
            gzip_data = reader.read_n_bytes(data_length // 8)  # 假设数据长度为比特数，因此除以 8

            try:
                # 使用 io.BytesIO 将字节数据包装成类似文件对象
                with io.BytesIO(bytes(gzip_data)) as byte_stream:
                    with gzip.GzipFile(fileobj=byte_stream) as f:
                        decompressed_data = f.read()

                # 解压后的数据解析为 JSON
                json_string = decompressed_data.decode('utf-8')
                return json.loads(json_string)

            except OSError as e:
                print(f"Gzip 解压缩错误: {e}")
            except Exception as e:
                print(f"解压或解析数据时出错: {e}")
        else:
            print("魔术数字不匹配")

        return None

    @staticmethod
    def main(image_path: Union[str, io.BytesIO]) -> Union[dict, None]:
        """主函数，集成上述操作，支持文件路径和文件对象"""
        # 加载图片
        img = Reading_Steganography.load_image(image_path)

        # 提取最低有效位
        lowest_data = Reading_Steganography.extract_lsb(img)

        # 获取魔术数字
        magic_string = Reading_Steganography.get_magic_string(lowest_data, Reading_Steganography.MAGIC_NUMBER)

        # 如果魔术数字匹配，则提取隐藏数据
        if magic_string == Reading_Steganography.MAGIC_NUMBER:
            json_data = Reading_Steganography.extract_stealth_data(lowest_data)
            if json_data:
                #print(f"解析的 JSON data: {json_data}")
                return json_data
            return None

if __name__ == "__main__":
    # 支持通过文件路径或文件对象测试
    image_path = io.BytesIO(open(r"D:\xm\img-jx\output\3_with_metadata.png", "rb").read())  # 或者文件对象

    # 不需要实例化类，直接调用静态方法
    Reading_Steganography.main(image_path)
