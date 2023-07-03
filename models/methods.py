from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from models.models import User


async def get_user(user_id: int, session: sessionmaker) -> User:
    async with session() as session:
        async with session.begin():
            return await session.execute(select(User).where(User.user_id == user_id)).one_or_none()
