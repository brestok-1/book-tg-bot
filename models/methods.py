from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select

from config_data.db_config import redis
from models.models import User, Book


async def get_user(user_id: int, session: async_sessionmaker):
    async with session() as session:
        async with session.begin():
            user = await session.execute(select(User).where(User.user_id == user_id))
            return user.first()


async def get_book_content(slug: str, session: AsyncSession) -> str:
    book = await session.get(Book, slug)
    content = book.content
    return content


async def is_user_exist(user_id: int, session: async_sessionmaker):
    res = await redis.get(name=f'is_user_exists:{str(user_id)}')
    if not res:
        async with session() as session:
            sql_res = await session.execute(select(User).where(User.user_id == user_id))
            sql_res = sql_res.one_or_none()
            await redis.set(name=f'is_user_exists:{str(user_id)}', value=1 if sql_res else 0)
            return bool(sql_res)
    else:
        return bool(res)


async def create_user(user_id: int, session: async_sessionmaker):
    async with session() as session:
        user = User(user_id=user_id)
        session.add(user)
        await session.commit()
