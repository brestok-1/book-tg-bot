import re
from config_data.config import PAGE_SIZE
from external_services.books_api import get_book_content


def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    clean_text = _clear_text(text)[start:start + size + 1]
    end_index = [i.end() for i in re.finditer(r'[,.!:;?]+', clean_text)]
    final_index = end_index[-1] if end_index[-1] <= size else end_index[-2]
    final_text = clean_text[:final_index]
    return final_text, len(final_text)


def _clear_text(text: str) -> str:
    clean_text = re.sub(r'\[\d]', '', text)
    return clean_text


def prepare_book(content: str) -> dict[int:str]:
    book_dict = {}
    number = 1
    text, end_index = _get_part_text(content, 0, PAGE_SIZE)
    while True:
        try:
            book_dict[number] = text.strip()
            text, index = _get_part_text(content, end_index, PAGE_SIZE)
            end_index += index
            number += 1
        except Exception:
            return book_dict


if __name__ == '__main__':
    text = get_book_content('kapitanskaya-dochka')
    diction = prepare_book(text)
    for k, v in diction.items():
        print(f'{k} - {v}')
