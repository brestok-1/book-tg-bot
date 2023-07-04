from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from lexicon.lexicon_en import LEXICON
from models.methods import get_user
from models.models import User

router = Router()


#
@router.message(CommandStart())
async def process_start_command(message: Message, **kwargs):
    user_id = message.from_user.id
    session = kwargs['session_maker']
    user = await get_user(user_id, session)
    if not user:
        user = User(user_id=user_id)
        async with session() as session:
            await session.add(user)
            await session.commit()


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(LEXICON['/help'])

#
# async def process_beginning_command(message:Message):
#     user = session.query(User).filter(User.id == message.from_user.id).first
#     user.page = 0
