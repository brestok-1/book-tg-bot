import re

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_en import LEXICON


def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    kp_builder = InlineKeyboardBuilder()
    kp_builder.row(*[InlineKeyboardButton(text=LEXICON[button] if button in LEXICON else button,
                                          callback_data=button if button in LEXICON else 'contents')
                     for button in buttons])
    kp_builder.row(InlineKeyboardButton(text=LEXICON['add_bookmark'], callback_data='add_to_bookmarks'))
    kp_builder.add(InlineKeyboardButton(text=LEXICON['back_to_library'], callback_data='books'))
    return kp_builder.as_markup()


def create_contents_keyboard(title: str, contents_page: int, book_dict:dict) -> InlineKeyboardMarkup:
    try:
        book_dict = dict(list(book_dict.items())[contents_page:contents_page + 15])
    except IndexError:
        book_dict = dict(list(book_dict.items())[contents_page:])
    kp_builder = InlineKeyboardBuilder()
    for k, v in book_dict.items():
        text = re.sub(r'\n', ' ', v[:200])
        kp_builder.row(InlineKeyboardButton(
            text=f'{k} — {text}',
            callback_data=k
        ), width=1)
    kp_builder.row(InlineKeyboardButton(text=LEXICON['backward'], callback_data='backward_contents'), width=1)
    kp_builder.add(InlineKeyboardButton(text=LEXICON['back_to_book'], callback_data=f'book_{title}'))
    kp_builder.add(InlineKeyboardButton(text=LEXICON['forward'], callback_data='forward_contents'))
    return kp_builder.as_markup()
