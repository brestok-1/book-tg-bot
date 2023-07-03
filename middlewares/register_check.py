from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select

from sqlalchemy.orm import sessionmaker

from models.models import User


class RegisterCheck(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        session_maker: sessionmaker = data['sessionmaker']
        async with session_maker() as session:
            async with session.begin():
                result = await session.execute(select(User).where(User.user_id == event.from_user.id))
                user: User = result.one_or_none()

                if user is not None:
                    pass
                else:
                    user = User(
                        user_id=event.from_user.id
                    )
                    await session.merge(user)
                    if isinstance(event, Message):
                        await event.answer('You have been successfully registered')
                    else:
                        await event.message.answer('You have been successfully registered')
        return await handler(event, data)
