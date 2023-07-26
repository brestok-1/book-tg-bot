import re

from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, delete
from sqlalchemy.sql.expression import and_
from keyboards.bookmarks import create_bookmarks_keyboard, create_edit_keyboard
from keyboards.books import create_books_keyboard
from keyboards.pagination import create_pagination_keyboard, create_contents_keyboard
from lexicon.lexicon_en import LEXICON
from models.methods import get_user
from models.models import User, Bookmark, Book
from services.book_handing import prepare_book
from filters.filters import DelCallbackFactory, IsDigitCallbackData, BookCallbackFactory

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
        await message.answer('You have been successfully registered')
    await message.answer(LEXICON['/start'])


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(LEXICON['/help'])


@router.message(Command(commands=['books']))
@router.callback_query(Text(text=['books']))
async def process_books_command(response: Message | CallbackQuery, **kwargs):
    session = kwargs['session_maker']
    async with session() as session:
        books = await session.execute(select(Book))
        books = books.scalars().all()
    if isinstance(response, Message):
        await response.answer(text=LEXICON['/books'], reply_markup=create_books_keyboard(books))
    else:
        await response.message.edit_text(text=LEXICON['/books'], reply_markup=create_books_keyboard(books))


@router.callback_query(lambda cb: cb.data.startswith('book_'))
async def get_necessary_book(callback: CallbackQuery, **kwargs):
    title = re.sub(r'book_', '', callback.data)
    session = kwargs['session_maker']
    async with session() as session:
        book_dict = await prepare_book(title, session)
        total_pages = list(book_dict.keys())[-1]
        user = await session.get(User, callback.from_user.id)
        user.contents_page = 0
        if user.active_book == '' or user.active_book != title:
            user.page = 1
            user.active_book = title
            current_page = user.page
            session.add(user)
            text = book_dict[current_page]
        else:
            current_page = user.page
            text = book_dict[current_page]
        await session.commit()
    await callback.message.edit_text(text=text,
                                     reply_markup=create_pagination_keyboard('backward',
                                                                             f'{current_page} / {total_pages}',
                                                                             'forward'))


@router.callback_query(Text(text=['forward']))
async def process_backward_command(callback: CallbackQuery, **kwargs):
    session = kwargs['session_maker']
    async with session() as session:
        user = await session.get(User, callback.from_user.id)
        book_dict = await prepare_book(user.active_book, session)
        total_pages = list(book_dict.keys())[-1]
        if user.page < int(total_pages):
            user.page += 1
            current_page = user.page
            text = book_dict[current_page]
            session.add(user)
            await session.commit()
            await callback.message.edit_text(text=text,
                                             reply_markup=create_pagination_keyboard('backward',
                                                                                     f'{current_page} / {total_pages}',
                                                                                     'forward'))
        else:
            await callback.answer(text=LEXICON['max_page'])


@router.callback_query(Text(text=['backward']))
async def process_backward_command(callback: CallbackQuery, **kwargs):
    session = kwargs['session_maker']
    async with session() as session:
        user = await session.get(User, callback.from_user.id)
        book_dict = await prepare_book(user.active_book, session)
        total_pages = list(book_dict.keys())[-1]
        if user.page > 1:
            user.page -= 1
            current_page = user.page
            text = book_dict[current_page]
            session.add(user)
            await session.commit()
            await callback.message.edit_text(text=text,
                                             reply_markup=create_pagination_keyboard('backward',
                                                                                     f'{current_page} / {total_pages}',
                                                                                     'forward'))
        else:
            await callback.answer(text=LEXICON['min_page'])


@router.callback_query(Text(text=['contents']))
async def show_contents(callback: CallbackQuery, **kwargs):
    session = kwargs['session_maker']
    async with session() as session:
        user = await session.get(User, callback.from_user.id)
        book_dict = await prepare_book(user.active_book, session)
        await callback.message.edit_text(text=LEXICON['contents'],
                                         reply_markup=create_contents_keyboard(user.active_book, user.contents_page,
                                                                               book_dict))


@router.callback_query(IsDigitCallbackData())
async def get_necessary_page(callback: CallbackQuery, **kwargs):
    session = kwargs['session_maker']
    async with session() as session:
        user = await session.get(User, callback.from_user.id)
        user.page = current_page = int(callback.data)
        book_dict = await prepare_book(user.active_book, session)
        session.add(user)
        await session.commit()
        total_pages = list(book_dict.keys())[-1]
        text = book_dict[current_page]
    await callback.message.edit_text(text=text,
                                     reply_markup=create_pagination_keyboard('backward',
                                                                             f'{current_page} / {total_pages}',
                                                                             'forward'))


@router.callback_query(Text(text=['backward_contents']))
async def process_backward_contents(callback: CallbackQuery, **kwargs):
    session = kwargs['session_maker']
    async with session() as session:
        user = await session.get(User, callback.from_user.id)
        book_dict = await prepare_book(user.active_book, session)
        if user.contents_page >= 15:
            user.contents_page -= 15
            session.add(user)
            await callback.message.edit_text(text=LEXICON['contents'],
                                             reply_markup=create_contents_keyboard(user.active_book,
                                                                                   user.contents_page, book_dict))
            await session.commit()
        else:
            await callback.answer(text=LEXICON['min_page'])


@router.callback_query(Text(text=['forward_contents']))
async def process_forward_contents(callback: CallbackQuery, **kwargs):
    session = kwargs['session_maker']
    async with session() as session:
        user = await session.get(User, callback.from_user.id)
        book_dict = await prepare_book(user.active_book, session)
        if user.contents_page <= list(book_dict.keys())[-1] - 15:
            user.contents_page += 15
            session.add(user)
            await callback.message.edit_text(text=LEXICON['contents'],
                                             reply_markup=create_contents_keyboard(user.active_book,
                                                                                   user.contents_page, book_dict))
            await session.commit()
        else:
            await callback.answer(text=LEXICON['max_page'])


@router.message(Command(commands=['beginning']))
async def process_beginning_command(message: Message, **kwargs):
    session = kwargs['session_maker']
    async with session() as session:
        user = await session.get(User, message.from_user.id)
        if user.active_book:
            book_dict = await prepare_book(user.active_book, session)
            total_pages = list(book_dict.keys())[-1]
            user.page = 1
            session.add(user)
            await message.answer(text=book_dict[1],
                                 reply_markup=create_pagination_keyboard('backward',
                                                                         f'{user.page} / {total_pages}',
                                                                         'forward'))
            await session.commit()
        else:
            await message.answer(LEXICON['None_page'])


@router.message(Command(commands=['continue']))
@router.callback_query(Text(text='continue'))
async def process_continue_command(response: Message | CallbackQuery, **kwargs):
    session = kwargs['session_maker']
    async with session() as session:
        user = await session.get(User, response.from_user.id)
        if user.active_book:
            book_dict = await prepare_book(user.active_book, session)
            total_pages = list(book_dict.keys())[-1]
            if isinstance(response, Message):
                await response.answer(text=book_dict[1],
                                      reply_markup=create_pagination_keyboard('backward',
                                                                              f'{user.page} / {total_pages}',
                                                                              'forward'))
            else:
                await response.message.edit_text(text=book_dict[1],
                                                 reply_markup=create_pagination_keyboard('backward',
                                                                                         f'{user.page} / {total_pages}',
                                                                                         'forward'))
        else:
            if isinstance(response, Message):
                await response.answer(LEXICON['None_page'])
            else:
                await response.answer()
                await response.message.answer(LEXICON['None_page'])


@router.callback_query(Text(text=['add_to_bookmarks']))
async def add_to_bookmarks(callback: CallbackQuery, **kwargs):
    session = kwargs['session_maker']
    async with session() as session:
        user = await session.get(User, callback.from_user.id)
        bookmark = await session.execute(
            select(Bookmark).filter(
                Bookmark.book == user.active_book,
                Bookmark.page == user.page,
                Bookmark.user_id == user.user_id
            )
        )
        bookmark = bookmark.one_or_none()
        if not bookmark:
            bookmark = Bookmark(user_id=user.user_id,
                                user=user,
                                book=user.active_book,
                                page=user.page)
            session.add(bookmark)
            await session.commit()
            await callback.answer('The bookmark was created successfully')
        else:
            await callback.answer('The bookmark was created earlier')


@router.message(Command(commands=['bookmarks']))
@router.callback_query(Text(text='bookmarks'))
async def get_bookmarks_list(response: Message | CallbackQuery, **kwargs):
    session = kwargs['session_maker']
    async with session() as session:
        bookmarks = await session.execute(select(Bookmark).where(Bookmark.user_id == response.from_user.id))
        bookmarks = bookmarks.scalars().all()
        if bookmarks:
            if isinstance(response, Message):
                await response.answer(text=LEXICON['/bookmarks'],
                                      reply_markup=create_bookmarks_keyboard(bookmarks))
            else:
                await response.message.edit_text(text=LEXICON['/bookmarks'],
                                                 reply_markup=create_bookmarks_keyboard(bookmarks))
        else:
            if isinstance(response, Message):
                await response.answer(LEXICON['no_bookmarks'])
            else:
                await response.message.edit_text(LEXICON['no_bookmarks'])


@router.callback_query(Text(text='edit_bookmarks'))
async def process_edit_press(callback: CallbackQuery, **kwargs):
    session = kwargs['session_maker']
    async with session() as session:
        bookmarks = await session.execute(select(Bookmark).where(Bookmark.user_id == callback.from_user.id))
        bookmarks = bookmarks.scalars().all()
        await callback.message.edit_text(text=LEXICON['edit_bookmarks'],
                                         reply_markup=create_edit_keyboard(bookmarks))


@router.callback_query(DelCallbackFactory.filter())
async def process_del_bookmark(callback: CallbackQuery, callback_data: DelCallbackFactory, **kwargs):
    session = kwargs['session_maker']
    async with session() as session:
        await session.execute(delete(Bookmark).where(
            and_(
                Bookmark.book == callback_data.book,
                Bookmark.page == int(callback_data.page)
            )
        ))
        bookmarks = await session.execute(select(Bookmark).where(Bookmark.user_id == callback.from_user.id))
        bookmarks = bookmarks.scalars().all()
        await callback.message.edit_text(text=LEXICON['edit_bookmarks'],
                                         reply_markup=create_edit_keyboard(bookmarks))
        await session.commit()


@router.callback_query(BookCallbackFactory.filter())
async def view_necessary_bookmark(callback: CallbackQuery, callback_data: DelCallbackFactory, **kwargs):
    session = kwargs['session_maker']
    async with session() as session:
        user = await session.get(User, callback.from_user.id)
        user.page = callback_data.page
        user.active_book = callback_data.book
        book_dict = await prepare_book(user.active_book, session)
        total_pages = list(book_dict.keys())[-1]
        session.add(user)
        await callback.message.edit_text(text=book_dict[callback_data.page],
                                         reply_markup=create_pagination_keyboard('backward',
                                                                                 f'{user.page} / {total_pages}',
                                                                                 'forward'))
        await session.commit()
