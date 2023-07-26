from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from external_services.books_api import Book


def create_books_keyboard(books: list[Book]) -> InlineKeyboardMarkup:
    kp_builder = InlineKeyboardBuilder()
    for i in books:
        kp_builder.row(InlineKeyboardButton(text=f'{i.title} — {i.author}', callback_data=f'book_{i.title}'), width=1)
    kp_builder.row(InlineKeyboardButton(text='BOOKMARKS', callback_data='bookmarks'), width=2)
    kp_builder.add(InlineKeyboardButton(text='CONTINUE', callback_data='continue'))
    return kp_builder.as_markup()

