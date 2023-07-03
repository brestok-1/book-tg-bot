import json
from pprint import pprint

import requests


def get_all_books_title_slug() -> dict:
    data = _get_api_data()
    dict_title_slug = _parse_title_slug(data)
    return dict_title_slug


def _get_api_data() -> list[dict]:
    response = requests.get('http://127.0.0.1:8000/api/books/')
    return json.loads(response.text)


def _parse_title_slug(data: list[dict]) -> dict:
    dict_title_slug = {}
    for i in data:
        dict_title_slug[i['title']] = i['slug']
    return dict_title_slug


def get_book_content(slug: str) -> str:
    content = _get_detail_api_data(slug)['content']
    return content


def _get_detail_api_data(slug: str) -> dict:
    response = requests.get(f'http://127.0.0.1:8000/api/books/{slug}/')
    return json.loads(response.text)


if __name__ == '__main__':
    pprint(_get_api_data())
    print(get_all_books_title_slug())
    print(get_book_content('kapitanskaya-dochka'))
