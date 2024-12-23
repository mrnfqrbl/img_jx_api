from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB 配置
MONGO_DETAILS = "mongodb://mrnf:mrnfqrbl@192.168.1.115:27019"
# 初始化 MongoDB 客户端
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.img  # 选择数据库
collection = database.images  # 选择集合，用于存储图片元数据

# 初始化数据库（MongoDB 自动创建集合）
async def init_db():
    # MongoDB 会在第一次插入数据时自动创建集合
    # 你可以在这里配置索引或验证规则（如需要）
    pass  # MongoDB 不需要显式创建表（集合），除非你需要设置索引等