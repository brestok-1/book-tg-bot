from dataclasses import dataclass
from environs import Env
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


env = Env()


def load_config(path: str | None = None) -> Config:
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')))


PAGE_SIZE = 1050

Base = declarative_base()


def get_async_engine(url: URL | str) -> AsyncEngine:
    return create_async_engine(url=url, echo=True, pool_pre_ping=True)


async def proceed_schemas(engine: AsyncEngine, metadata):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


def get_async_sessionmaker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

#
# engine = create_engine('postgresql://postgres:password@db/book_tg_users')
# Base.metadata.create_all(engine)
#
# Session = sessionmaker(bind=engine)
# session = Session()
