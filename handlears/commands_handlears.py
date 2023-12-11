from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from filters.filters_commands import (
    HelpCommand,
    MyBooksCommand,
    MyBooksMarksCommand,
    ContinueReadCommand
)

from database.requests import DataBaseRequests
from database.models import get_session

from lexicon.lexicon_ru import LEXICON_RU
from keyboards.main_keyboard import get_main_keyboard

from keyboards.inline_keyboards.get_inlines_keyboards import (
    get_user_books_inline_kb,
    get_user_books_marks_inline_kb,
    get_pagination_kb
)

from handlears.callbacks_handlears import text_formatting

router = Router()
requests_db = DataBaseRequests(session=get_session())

@router.message(CommandStart())
async def start_command(message: Message):
    user_name = message.from_user.first_name.strip()
    if not await requests_db.exists_user(username=user_name):
        await requests_db.insert_user(username=user_name)

    await message.answer(
        text=LEXICON_RU['start'](user_name),
        reply_markup=get_main_keyboard()
    )

@router.message(HelpCommand())
async def help_command(message: Message, key: str):
    await message.answer(
        text=LEXICON_RU[key],
        reply_markup=get_main_keyboard()
    )


@router.message(MyBooksCommand())
async def my_books_command(message: Message, key: str):
    name = message.from_user.first_name.strip()
    books = await requests_db.select_books_user(username=name)

    if not books:
        return await message.answer(
            text=LEXICON_RU['empty_' + key]
        )

    await message.answer(
        text=LEXICON_RU['exists_' + key],
        reply_markup=get_user_books_inline_kb(user_books=books)
    )


@router.message(MyBooksMarksCommand())
async def my_books_marks_command(message: Message, key: str):
    name = message.from_user.first_name.strip()
    books_marks = await requests_db.select_book_marks_user(username=name)

    if not books_marks:
        return await message.answer(
            text=LEXICON_RU['empty_' + key]
        )

    await message.answer(
        text=LEXICON_RU['exists_' + key],
        reply_markup=get_user_books_marks_inline_kb(user_books_marks=books_marks)
    )

@router.message(ContinueReadCommand())
async def continue_read_command(
    message: Message,
    book_name: str | None,
    book_content: str | None,
    last_page: int | None,
    no_continue_text: str | None
):

    if no_continue_text:
        return await message.answer(text=no_continue_text)

    text_formatting.format_book_text(
        text=book_content,
        book=book_name
    )

    await message.answer(
        text=text_formatting.ready_text[last_page],
        reply_markup=get_pagination_kb(
            number_page=last_page,
            number_pagination=text_formatting.last_text_page,
            book_name=book_name
        )
    )
