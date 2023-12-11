from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from database.requests import DataBaseRequests
from database.models import get_session

requests_db = DataBaseRequests(session=get_session())

class UserBookCallBackFilter(BaseFilter):

    async def __call__(self, callback: CallbackQuery) -> Any:
        if callback.data.startswith('bookcall'):
            username = callback.from_user.first_name.strip()
            user_books = await requests_db.select_books_user(username=username)
            call_data_book = callback.data.split(':')[-1]

            for book in user_books:
                if book == call_data_book:
                    return {
                        'book_info': user_books[book],
                        'book_name': call_data_book
                    }

        return False

class UserBookMarkCallBackFilter(BaseFilter):

    async def __call__(self, callback: CallbackQuery) -> Any:
        if callback.data.startswith('bookmarkcall'):
            book_and_book_mark_page = callback.data.split(':')

            username = callback.from_user.first_name.strip()
            book_name = book_and_book_mark_page[1]
            book_mark_page = int(book_and_book_mark_page[-1])
            user_books = await requests_db.select_books_user(username=username)

            for book in user_books:
                if book == book_name:
                    return {
                        'book_mark_page': book_mark_page,
                        'book_info': user_books[book],
                        'book_name': book_name
                    }

        return False

class CenterButtonCallBackFilter(BaseFilter):

    async def __call__(self, callback: CallbackQuery) -> Any:
        if callback.data.startswith('center'):
            new_book_mark = callback.data.split(':')
            page = int(new_book_mark[1])
            book = new_book_mark[-1]

            return {
                'page': page,
                'book': book
            }

        else:
            return False

class ForwardButtonCallBackFilter(BaseFilter):

    async def __call__(self, callback: CallbackQuery) -> Any:
        if callback.data.startswith('forward'):
            new_page = callback.data.split(':')
            next_page = int(new_page[1]) + 1
            book = new_page[-1]

            return {
                'next_page': next_page,
                'book': book
            }

        else:
            return False

class BackwardButtonCallBackFilter(BaseFilter):

    async def __call__(self, callback: CallbackQuery) -> Any:
        if callback.data.startswith('backward'):
            new_page = callback.data.split(':')
            previous_page = int(new_page[1]) - 1
            book = new_page[-1]

            return {
                'previous_page': previous_page,
                'book': book
            }

        else:
            return False

class UserDeleteBookCallBackFilter(BaseFilter):

    async def __call__(self, callback: CallbackQuery) -> Any:
        if callback.data.startswith('booksedit'):
            book = callback.data.split(':')[-1]
            user = callback.from_user.first_name.strip()

            return {
                'username': user,
                'book_name': book
            }

        return False

class UserDeleteBookMarkCallBackFilter(BaseFilter):

    async def __call__(self, callback: CallbackQuery) -> Any:
        if callback.data.startswith('bookmarksedit'):
            data_info = callback.data.split(':')

            username = callback.from_user.first_name.strip()
            book_name = data_info[1]
            page = int(data_info[-1])

            return {
                'username': username,
                'book_name': book_name,
                'page': page
            }

        return False

__all__ = (
    'UserBookCallBackFilter',
    'UserBookMarkCallBackFilter',
    'CenterButtonCallBackFilter',
    'ForwardButtonCallBackFilter',
    'BackwardButtonCallBackFilter',
    'UserDeleteBookCallBackFilter',
    'UserDeleteBookMarkCallBackFilter'
)
