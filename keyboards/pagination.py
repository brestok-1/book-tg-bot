from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_en import LEXICON


def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    kp_builder = InlineKeyboardBuilder()
    kp_builder.row(*[InlineKeyboardButton(text=LEXICON[button] if button in LEXICON else button,
                                          callback_data=button) for button in buttons])
    return kp_builder.as_markup()