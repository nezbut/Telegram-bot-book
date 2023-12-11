from aiogram.filters import BaseFilter
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_KEYBOARDS, LEXICON_RU
from database.requests import DataBaseRequests
from database.models import get_session

requests_db = DataBaseRequests(session=get_session())

class BaseCommandsFilter(BaseFilter):
    key = None

    async def __call__(self, message: Message) -> bool:
        key = LEXICON_KEYBOARDS['main_keyboard'][self.key]
        return {'key': key} if message.text and message.text.strip() == key else False

class ContinueReadCommand(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        key = LEXICON_KEYBOARDS['main_keyboard']['continue']

        if message.text and message.text.strip() == key:
            username = message.from_user.first_name.strip()
            user_continue_read_book = await requests_db.get_continue_book(username=username)

            return {
                'book_name': user_continue_read_book['book_name'],
                'book_content': user_continue_read_book['content_book'],
                'last_page': user_continue_read_book['last_page'],
                'no_continue_text': None
            } if user_continue_read_book else {
                'book_name': None,
                'book_content': None,
                'last_page': None,
                'no_continue_text': LEXICON_RU['no_continue_read_book']
            }

        return False

class HelpCommand(BaseCommandsFilter):
    key = 'help_bot'


class MyBooksCommand(BaseCommandsFilter):
    key = 'my_books'


class MyBooksMarksCommand(BaseCommandsFilter):
    key = 'my_books_marks'

__all__ = (
    'HelpCommand',
    'MyBooksCommand',
    'MyBooksMarksCommand',
    'ContinueReadCommand'
)
