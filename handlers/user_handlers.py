from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from external_services.books_api import get_all_books, get_book_content, get_all_slugs
from keyboards.books import create_books_keyboard
from keyboards.pagination import create_pagination_keyboard
from lexicon.lexicon_en import LEXICON
from models.methods import get_user
from models.models import User
from services.book_handing import prepare_book

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
            session.add(user)
            await session.commit()
    else:
        await message.answer(LEXICON['/start'])


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(LEXICON['/help'])


@router.message(Command(commands=['books']))
async def process_books_command(message: Message):
    books = get_all_books()
    await message.answer(text=LEXICON['/books'], reply_markup=create_books_keyboard(books))


@router.callback_query(Text(text=get_all_slugs()))
async def get_necessary_book(callback: CallbackQuery):
    slug = callback.data
    necessary_book = get_book_content(slug)
    book_dict = prepare_book(necessary_book)
    await callback.message.edit_text(text=book_dict[1],
                                     reply_markup=create_pagination_keyboard('backward', f'CurrentPage  ', 'forward'))
# async def process_beginning_command(message:Message):
#     user = session.query(User).filter(User.id == message.from_user.id).first
#     user.page = 0
