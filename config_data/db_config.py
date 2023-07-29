from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from aioredis import Redis

from config_data.config import env


def get_async_engine(url: URL | str) -> AsyncEngine:
    return create_async_engine(url=url, echo=True, pool_pre_ping=True)


@DeprecationWarning
async def proceed_schemas(engine: AsyncEngine, metadata):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


def get_async_sessionmaker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(bind=engine, class_=AsyncSession)


redis = Redis(host='localhost')
