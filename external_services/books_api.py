import json
from dataclasses import dataclass
import requests


@dataclass
class Book:
    title: str
    slug: str
    content: str
    author: str

    def __eq__(self, other):
        if isinstance(other, Book):
            return (
                    self.title == other.title and
                    self.content == other.content and
                    self.author == other.author
            )
        return False


def get_all_books():
    data = _get_api_data()
    books = _parse_books_data(data)
    return books


def _parse_books_data(data: list[dict]) -> list[Book]:
    books = []
    for i in data:
        title = i['title']
        slug = i['slug']
        content = i['content']
        author = i['author']
        books.append(Book(title, slug, content, author))
    return books


def _get_api_data() -> list[dict]:
    response = requests.get('http://0.0.0.0:8000/api/books/')
    return json.loads(response.text)
