from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from aioredis import Redis
from sqlalchemy.engine import URL
from config_data.config import env


def get_async_engine(url: str) -> AsyncEngine:
    return create_async_engine(url=url, echo=True, pool_pre_ping=True)


@DeprecationWarning
async def proceed_schemas(engine: AsyncEngine, metadata):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


def get_async_sessionmaker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(bind=engine, class_=AsyncSession)


POSTGRES_URL = URL.create(
        "postgresql+asyncpg",
        username=env('POSTGRES_USER'),
        password=env('POSTGRES_PASSWORD'),
        host=env('POSTGRES_HOST'),
        database=env('POSTGRES_DB'),
        port=env('POSTGRES_PORT'),
    )


redis = Redis(host=env('REDIS_HOST'))
