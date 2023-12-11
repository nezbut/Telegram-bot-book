from aiogram.types import CallbackQuery
from lexicon.lexicon_ru import LEXICON_KEYBOARDS, LEXICON_RU
from database.requests import DataBaseRequests
from keyboards.inline_keyboards.get_inlines_keyboards import get_user_books_inline_kb

async def if_book_not_read(callback: CallbackQuery, requests_db: DataBaseRequests):
    name = callback.from_user.first_name.strip()
    books = await requests_db.select_books_user(username=name)

    await edit_text_user_books(callback=callback, books=books)

    await callback.answer(
        text=LEXICON_RU['if_book_not_read']
    )

async def edit_text_user_books(callback: CallbackQuery, books: dict):
    await callback.message.edit_text(
        text=LEXICON_RU['exists_' + LEXICON_KEYBOARDS['main_keyboard']['my_books']],
        reply_markup=get_user_books_inline_kb(user_books=books)
    )

__all__ = (
    'if_book_not_read',
    'edit_text_user_books'
)
