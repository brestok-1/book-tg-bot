from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select

from sqlalchemy.ext.asyncio import async_sessionmaker

from models.methods import is_user_exist, create_user
from models.models import User


class RegisterCheck(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        session_maker: async_sessionmaker = data['session_maker']
        if not await is_user_exist(user_id=event.from_user.id, session=session_maker):
            await create_user(user_id=event.from_user.id, session=session_maker)
            await data['bot'].send_message(event.from_user.id, 'You have been successfully registered')
        return await handler(event, data)
