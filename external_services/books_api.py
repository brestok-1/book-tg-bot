import json
from pprint import pprint
from dataclasses import dataclass
import requests


@dataclass
class Book:
    title: str
    slug: str
    author: str


def get_all_books():
    data = _get_api_data()
    books = _parse_books_data(data)
    return books


def get_all_slugs() -> list:
    data = _get_api_data()
    slugs = _parse_slug_data(data)
    return slugs


def _parse_slug_data(data: list) -> list:
    slugs = [i['slug'] for i in data]
    return slugs


def _parse_books_data(data: list[dict]) -> list[Book]:
    books = []
    for i in data:
        title = i['title']
        slug = i['slug']
        author = i['author']
        books.append(Book(title, slug, author))
    return books


def _get_api_data() -> list[dict]:
    response = requests.get('http://0.0.0.0:8000/api/books/')
    return json.loads(response.text)


def get_book_content(slug: str) -> str:
    content = _get_detail_api_data(slug)['content']
    return content


def _get_detail_api_data(slug: str) -> dict:
    response = requests.get(f'http://127.0.0.1:8000/api/books/{slug}/')
    return json.loads(response.text)


if __name__ == '__main__':
    # pprint(_get_api_data())
    # print(get_book_content('kapitanskaya-dochka'))
    print(get_all_slugs())
    books = get_all_books()
    for i in books:
        print(f'{i.title} - {i.author} - {i.slug}')
