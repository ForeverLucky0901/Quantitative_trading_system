"""
数据库初始化脚本
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.core.database import Base
from app.models import *  # 导入所有模型


async def init_database():
    """初始化数据库"""
    print("正在初始化数据库...")
    
    # 创建异步引擎
    engine = create_async_engine(
        settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
        echo=True
    )
    
    # 创建所有表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # 删除所有表（开发环境）
        await conn.run_sync(Base.metadata.create_all)  # 创建所有表
    
    await engine.dispose()
    print("数据库初始化完成！")


if __name__ == "__main__":
    asyncio.run(init_database())
