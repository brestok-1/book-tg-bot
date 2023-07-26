from aiogram.filters import BaseFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery


class IsDigitCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery, *args, **kwargs):
        return isinstance(callback.data, str) and callback.data.isdigit()


class DelCallbackFactory(CallbackData, prefix='del'):
    book: str
    page: int


class BookCallbackFactory(CallbackData, prefix='book'):
    book: str
    page: int
