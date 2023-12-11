from aiogram import Router, F
from aiogram.types import Message

from filters.filter_file import TxTFileFilter
from database.models import get_session
from database.requests import DataBaseRequests
from lexicon.lexicon_ru import LEXICON_RU

router = Router()
requests_db = DataBaseRequests(session=get_session())

@router.message(TxTFileFilter())
async def txt_files_add_book_handlear(message: Message, username: str, book_name: str, book_content: str):

    if message.document.file_size > 17_900_000:
        return await message.answer(
            text=LEXICON_RU['big_size_file']
        )

    if await requests_db.exists_book_user(username=username, book=book_name):
        return await message.answer(
            LEXICON_RU['user_add_book_and_book_exists']
        )

    await requests_db.insert_book(
        book_name=book_name,
        content_book=book_content,
        user_book=username
    )

    await message.answer(
        text=LEXICON_RU['book_add']
    )

@router.message(F.document)
async def other_files_handlear(message: Message):
    await message.answer(
        text=LEXICON_RU['document_not_txt']
    )
