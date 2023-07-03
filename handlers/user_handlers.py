from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker

from lexicon.lexicon_en import LEXICON
from models.methods import get_user
from models.models import User

router = Router()


#
@router.message(CommandStart())
async def process_start_command(message: Message, session: sessionmaker):
    await message.answer(LEXICON['start'])
    user_id = message.from_user.id
    user = await get_user(user_id=user_id, session=session)
    if not user:
        user = User(id=user_id)
        session.add(user)
        session.commit()

#
# async def process_help_command(message: Message):
#     await message.answer(LEXICON['/help'])
#
#
# async def process_beginning_command(message:Message):
#     user = session.query(User).filter(User.id == message.from_user.id).first
#     user.page = 0
