from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.download_file import get_book_content_in_txt_file


class TxTFileFilter(BaseFilter):

    async def __call__(self, message: Message) -> Any:
        if message.document.file_name.strip().endswith('.txt'):
            doc = message.document
            username = message.from_user.first_name.strip()

            book_name = message.document.file_name.removesuffix('.txt').strip()
            book_content = await get_book_content_in_txt_file(
                bot=message.bot,
                txt_file_id=doc.file_id
            )

            return {
                'username': username,
                'book_name': book_name,
                'book_content': book_content
            }

        return False

__all__ = (
    'TxTFileFilter',
)
