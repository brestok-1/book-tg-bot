from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select

from models.models import User


async def get_user(user_id: int, session: async_sessionmaker):
    async with session() as session:
        async with session.begin():
            user = await session.execute(select(User).where(User.user_id == user_id))
            return user.first()

