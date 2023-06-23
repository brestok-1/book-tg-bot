from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon_en import LEXICON

router = Router()


@router.message()
async def process_other_commands(message: Message):
    await message.answer(f"{LEXICON['other_commands']}")
