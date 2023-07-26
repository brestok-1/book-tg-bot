import re

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from filters.filters import DelCallbackFactory, BookCallbackFactory
from lexicon.lexicon_en import LEXICON
from models.models import Bookmark


def create_bookmarks_keyboard(bookmarks: list[Bookmark]) -> InlineKeyboardMarkup:
    kp_builder = InlineKeyboardBuilder()
    for button in bookmarks:
        kp_builder.row(InlineKeyboardButton(
            text=f'{button.book} — {button.page} page',
            callback_data=BookCallbackFactory(book=button.book, page=button.page).pack()
        ))
    kp_builder.row(InlineKeyboardButton(text=LEXICON['edit_bookmarks_button'], callback_data='edit_bookmarks'),
                   InlineKeyboardButton(text=LEXICON['go_back'], callback_data='books'), width=2)
    return kp_builder.as_markup()


def create_edit_keyboard(bookmarks: list[Bookmark]) -> InlineKeyboardMarkup:
    kp_builder = InlineKeyboardBuilder()
    for button in bookmarks:
        kp_builder.row(InlineKeyboardButton(
            text=f'{LEXICON["del"]} {button.book} — {button.page} page',
            callback_data=DelCallbackFactory(book=button.book, page=button.page).pack()
        ))
    kp_builder.row(InlineKeyboardButton(text=LEXICON['go_back'], callback_data='bookmarks'))
    return kp_builder.as_markup()
