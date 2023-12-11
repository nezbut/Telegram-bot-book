from aiogram import Router, F
from aiogram.types import CallbackQuery

from filters.filters_callbacks import (
    UserBookCallBackFilter,
    UserBookMarkCallBackFilter,
    CenterButtonCallBackFilter,
    ForwardButtonCallBackFilter,
    BackwardButtonCallBackFilter,
    UserDeleteBookCallBackFilter,
    UserDeleteBookMarkCallBackFilter
)

from lexicon.lexicon_ru import LEXICON_RU, LEXICON_KEYBOARDS
from utils.book_text_formatting import BookTextFormatting
from handlears.utils_callbacks import if_book_not_read, edit_text_user_books
from database.requests import DataBaseRequests
from database.models import get_session

from keyboards.inline_keyboards.get_inlines_keyboards import (
    get_pagination_kb,
    get_edit_books_inline_kb,
    get_edit_book_marks_inline_kb,
    get_user_books_marks_inline_kb
)

router = Router()
text_formatting = BookTextFormatting()
requests_db = DataBaseRequests(session=get_session())

@router.callback_query(ForwardButtonCallBackFilter())
async def forward_button_callback(callback: CallbackQuery, next_page: int, book: str):
    if book != text_formatting.book_name:
        return await if_book_not_read(
            callback=callback,
            requests_db=requests_db
        )

    if next_page > text_formatting.last_text_page:
        return await callback.answer()

    username = callback.from_user.first_name.strip()

    await callback.message.edit_text(
        text=text_formatting.ready_text[next_page],
        reply_markup=get_pagination_kb(
            number_page=next_page,
            number_pagination=text_formatting.last_text_page,
            book_name=book
        )
    )

    await requests_db.update_book_last_page(
        username=username,
        book_name=book,
        new_last_page=next_page
    )

@router.callback_query(BackwardButtonCallBackFilter())
async def backward_button_callback(callback: CallbackQuery, previous_page: int, book: str):
    if book != text_formatting.book_name:
        return await if_book_not_read(
            callback=callback,
            requests_db=requests_db
        )

    if previous_page < 1:
        return await callback.answer()

    username = callback.from_user.first_name.strip()

    await callback.message.edit_text(
        text=text_formatting.ready_text[previous_page],
        reply_markup=get_pagination_kb(
            number_page=previous_page,
            number_pagination=text_formatting.last_text_page,
            book_name=book
        )
    )

    await requests_db.update_book_last_page(
        username=username,
        book_name=book,
        new_last_page=previous_page
    )

@router.callback_query(CenterButtonCallBackFilter())
async def center_button_callback(callback: CallbackQuery, page: int, book: str):
    username = callback.from_user.first_name.strip()
    result_request = await requests_db.exists_book_mark_user(username=username, book=book, num_bk=page)

    if result_request:
        return await callback.answer(
            text=LEXICON_RU['exists_book_mark']
        )

    await requests_db.insert_book_mark(
        bookmark_for_book=book,
        user=username,
        num_bookmark=page
    )

    await callback.answer(
        text=LEXICON_RU['good_add_book_mark']
    )

@router.callback_query(UserBookCallBackFilter())
async def user_book_callback(callback: CallbackQuery, book_info: dict, book_name: str):
    book_content = book_info.get('content')
    book_last_page = book_info.get('last_page')
    username = callback.from_user.first_name.strip()

    text_formatting.format_book_text(text=book_content, book=book_name)

    await callback.message.edit_text(
        text=text_formatting.ready_text[book_last_page],
        reply_markup=get_pagination_kb(
            number_page=book_last_page,
            number_pagination=text_formatting.last_text_page,
            book_name=book_name
        )
    )

    await callback.answer(
        text=LEXICON_RU['enjoy_reading']
    )

    await requests_db.update_continue_status_book(
        username=username,
        book_name=book_name
    )

@router.callback_query(UserBookMarkCallBackFilter())
async def user_book_mark_callback(callback: CallbackQuery, book_mark_page: int, book_info: dict, book_name: str):
    book_content = book_info.get('content')
    username = callback.from_user.first_name.strip()

    text_formatting.format_book_text(text=book_content, book=book_name)

    await callback.message.edit_text(
        text=text_formatting.ready_text[book_mark_page],
        reply_markup=get_pagination_kb(
            number_page=book_mark_page,
            number_pagination=text_formatting.last_text_page,
            book_name=book_name
        )
    )

    await callback.answer(
        text=LEXICON_RU['enjoy_reading']
    )

    await requests_db.update_continue_status_book(
        username=username,
        book_name=book_name
    )

@router.callback_query(F.data == 'booksedit')
async def edit_books_callback(callback: CallbackQuery):
    username = callback.from_user.first_name.strip()
    books = await requests_db.select_books_user(username=username)

    await callback.message.edit_text(
        text=LEXICON_KEYBOARDS['edit'],
        reply_markup=get_edit_books_inline_kb(user_books=books)
    )

@router.callback_query(F.data == 'bookscancel')
async def cancel_button_books_callback(callback: CallbackQuery):
    username = callback.from_user.first_name.strip()
    books = await requests_db.select_books_user(username=username)

    await edit_text_user_books(
        callback=callback,
        books=books
    )

@router.callback_query(UserDeleteBookCallBackFilter())
async def user_delete_book_callback(callback: CallbackQuery, username: str, book_name: str):
    if not await requests_db.exists_book_user(username=username, book=book_name):
        return await callback.answer(
            text=LEXICON_RU['user_delete_book_and_book_not_exists']
        )

    await requests_db.delete_user_book(
        username=username,
        book_name=book_name
    )

    await callback.answer(
        text=LEXICON_RU['good_book_deleted']
    )

@router.callback_query(F.data == 'bookmarksedit')
async def edit_book_marks_callback(callback: CallbackQuery):
    username = callback.from_user.first_name.strip()
    user_book_marks = await requests_db.select_book_marks_user(username=username)

    await callback.message.edit_text(
        text=LEXICON_KEYBOARDS['edit'],
        reply_markup=get_edit_book_marks_inline_kb(
            user_books_marks=user_book_marks
        )
    )

@router.callback_query(F.data == 'bookmarkscancel')
async def cancel_button_book_marks_callback(callback: CallbackQuery):
    username = callback.from_user.first_name.strip()
    user_book_marks = await requests_db.select_book_marks_user(username=username)

    await callback.message.edit_text(
        text=LEXICON_RU['exists_' + LEXICON_KEYBOARDS['main_keyboard']['my_books_marks']],
        reply_markup=get_user_books_marks_inline_kb(
            user_books_marks=user_book_marks
        )
    )

@router.callback_query(UserDeleteBookMarkCallBackFilter())
async def user_delete_book_mark_callback(callback: CallbackQuery, username: str, book_name: str, page: int):
    if not await requests_db.exists_book_mark_user(username=username, book=book_name, num_bk=page):
        return await callback.answer(
            text=LEXICON_RU['user_delete_book_mark_and_book_mark_not_exists']
        )

    await requests_db.delete_user_book_mark(
        username=username,
        bookmark_for_book=book_name,
        page=page
    )

    await callback.answer(
        text=LEXICON_RU['good_book_mark_deleted']
    )
