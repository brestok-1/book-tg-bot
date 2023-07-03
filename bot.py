import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.engine import URL
from config_data.config import load_config, get_async_engine, proceed_schemas, get_async_sessionmaker, Base, env
from handlers import user_handlers, other_handlers
from keyboards.main_menu import set_main_menu
from middlewares.register_check import RegisterCheck


async def main():
    logging.basicConfig(level=logging.INFO, format='%(filename)s:%(lineno)d #%(levelname)-8s '
                                                   '[%(asctime)s] - %(name)s - %(message)s')
    logging.info('Starting Bot')
    config = load_config()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # dp.message.middleware(RegisterCheck)
    # dp.callback_query.middleware(RegisterCheck)

    await set_main_menu(bot)

    # postgres_url = URL.create(
    #     "postgresql+asyncpg",
    #     username=env('POSTGRES_USER'),
    #     password=env('POSTGRES_PASSWORD'),
    #     host=env('POSTGRES_HOST'),
    #     database=env('POSTGRES_DB'),
    #     port=env('POSTGRES_PORT'),
    # )
    # # postgres_url = 'postgresql+asyncpg://maksim:135799@localhost:5432/book_bot_users'
    # async_engine = get_async_engine(postgres_url)
    # session_maker = get_async_sessionmaker(async_engine)
    #
    # await proceed_schemas(async_engine, Base.metadata)
    =
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot has been stoped')
