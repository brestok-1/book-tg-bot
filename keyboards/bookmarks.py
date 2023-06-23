from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_en import LEXICON


def create_bookmarks_keyboard(book: str, *args: int) -> InlineKeyboardMarkup:
    kp_builder = InlineKeyboardBuilder()
    for button in sorted(args):
        kp_builder.row(InlineKeyboardButton(
            text=f'{button} - {book} - {book[button][:100]}',
            callback_data=str(button)
        ))
    kp_builder.row(InlineKeyboardButton(text=LEXICON['edit_bookmarks_button'], callback_data='edit_bookmarks'),
                   InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel'), width=2)
    return kp_builder.as_markup()


def create_edit_keyboard(book, *args) -> InlineKeyboardMarkup:
    kp_builder = InlineKeyboardBuilder()
    for button in sorted(args):
        kp_builder.row(InlineKeyboardButton(
            text=f'{LEXICON["del"]} {button} - {book} - {book[button[:100]]}',
            callback_data=f'{button}del'
        ))
    kp_builder.row(InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel'))
    return kp_builder.as_markup()
