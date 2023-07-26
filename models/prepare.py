import aiocron
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select
from external_services.books_api import get_all_books
from models.models import Book
from requests.exceptions import ConnectionError


# @aiocron.crontab('*/10 * * * * *')
async def initialize_book_data(session: async_sessionmaker):
    try:
        books = get_all_books()
        async with session() as session:
            db_books = await session.execute(select(Book))
            db_books = db_books.scalars().all()
            for book in books:
                book = Book(
                    title=book.title,
                    content=book.content,
                    author=book.author
                )
                if book not in db_books:
                    session.add(book)
            await session.commit()
    except ConnectionError:
        print('Connection refused')


async def scheduled_task(session: async_sessionmaker):
    await initialize_book_data(session)
