from aiogram.types import InlineKeyboardMarkup
from keyboards.inline_keyboards.builder import inline_keyboard_builder
from lexicon.lexicon_ru import LEXICON_KEYBOARDS, LEXICON_RU

def get_user_books_inline_kb(user_books: dict) -> InlineKeyboardMarkup:
    return inline_keyboard_builder(
        1,
        callback_and_text_dict={
            f'bookcall:{book_name}': f"{book_name} | {book_info.get('content')[:100] + '...' if len(book_info.get('content')) > 100 else book_info.get('content')}" for book_name, book_info in user_books.items()
        },
        last_buttons={"booksedit": LEXICON_KEYBOARDS['edit']}
    )

def get_user_books_marks_inline_kb(user_books_marks: dict) -> InlineKeyboardMarkup:
    result_dict = {}

    for book_name, book_marks in user_books_marks.items():

        for book_mark in sorted(book_marks):
            result_dict.update({f'bookmarkcall:{book_name}:{book_mark}': f"{book_name} | Страница: {book_mark}"})

    return inline_keyboard_builder(
        1,
        callback_and_text_dict=result_dict,
        last_buttons={"bookmarksedit": LEXICON_KEYBOARDS['edit']}
    )

def get_pagination_kb(number_page: int, number_pagination: int, book_name: str) -> InlineKeyboardMarkup:
    buttons_dict = {
        f'backward:{number_page}:{book_name}': LEXICON_KEYBOARDS['backward'],
        f'center:{number_page}:{book_name}': f"{number_page}/{number_pagination}",
        f'forward:{number_page}:{book_name}': LEXICON_KEYBOARDS['forward']
    }

    return inline_keyboard_builder(width=3, callback_and_text_dict=buttons_dict)

def get_edit_books_inline_kb(user_books: dict) -> InlineKeyboardMarkup:
    return inline_keyboard_builder(
        1,
        callback_and_text_dict={
            f'booksedit:{book_name}': f"❌{LEXICON_RU['delete']}: {book_name}" for book_name in user_books
        },
        last_buttons={"bookscancel": LEXICON_KEYBOARDS['cancel']}
    )

def get_edit_book_marks_inline_kb(user_books_marks: dict) -> InlineKeyboardMarkup:
    result_dict = {}

    for book_name, book_marks in user_books_marks.items():

        for book_mark in sorted(book_marks):
            result_dict.update({f'bookmarksedit:{book_name}:{book_mark}': f"❌{LEXICON_RU['delete']}: {book_name} | {book_mark}"})

    return inline_keyboard_builder(
        1,
        callback_and_text_dict=result_dict,
        last_buttons={"bookmarkscancel": LEXICON_KEYBOARDS['cancel']}
    )

__all__ = (
    'get_user_books_marks_inline_kb',
    'get_user_books_inline_kb',
    'get_pagination_kb',
    'get_edit_books_inline_kb',
    'get_edit_book_marks_inline_kb'
)
