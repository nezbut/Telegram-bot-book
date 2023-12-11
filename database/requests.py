from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, Book, BookMark

class DataBaseRequests:

    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def insert_user(self, username: str):
        async with self.async_session() as session:
            session: AsyncSession

            new_user = User(username=username)
            session.add(new_user)

            await session.flush()
            await session.commit()

    async def insert_book(self, book_name: str, content_book: str, user_book: str):
        async with self.async_session() as session:
            session: AsyncSession

            new_book = Book(
                book_name=book_name,
                content_book=content_book,
                user_book=user_book
            )
            session.add(new_book)

            await session.flush()
            await session.commit()

    async def insert_book_mark(self, bookmark_for_book: str, user: str, num_bookmark: int):
        async with self.async_session() as session:
            session: AsyncSession

            new_book_mark = BookMark(
                bookmark_for_book=bookmark_for_book,
                user=user,
                num_bookmark=num_bookmark
            )
            session.add(new_book_mark)

            await session.flush()
            await session.commit()

    async def select_book_marks_user(self, username: str) -> dict[str, set[int]]:
        async with self.async_session() as session:
            session: AsyncSession

            result_dict: dict[str, set[int]] = {}
            query = select(BookMark).filter_by(user=username)
            result = await session.execute(query)

            for book_mark_obj in result.scalars().all():
                book = book_mark_obj.bookmark_for_book
                num = book_mark_obj.num_bookmark

                if not result_dict.get(book):
                    result_dict[book] = set()

                result_dict[book].add(num)

            return result_dict

    async def select_books_user(self, username: str) -> dict[str, dict[str, str | int | bool]]:
        async with self.async_session() as session:
            session: AsyncSession

            result_dict: dict[str, dict[str, str | int | bool]] = {}
            query = select(Book).filter_by(user_book=username)
            result = await session.execute(query)

            for book_obj in result.scalars().all():
                book_name = book_obj.book_name
                content = book_obj.content_book
                last_page = book_obj.last_page
                continue_read = book_obj.continue_read

                if not result_dict.get(book_name):
                    result_dict[book_name] = {}

                result_dict[book_name].update(
                    {
                        'content': content,
                        'last_page': last_page,
                        'continue': continue_read
                    }
                )

            return result_dict

    async def update_continue_status_book(self, username: str, book_name: str):
        async with self.async_session() as session:
            session: AsyncSession

            try:

                querys = [
                    update(Book).filter_by(user_book=username, continue_read=True).values(continue_read=False),
                    update(Book).filter_by(user_book=username, book_name=book_name).values(continue_read=True)
                ]

                for query in querys:
                    await session.execute(query)

                await session.commit()

            except Exception:
                return False

            else:
                return True

    async def update_book_last_page(self, username: str, book_name: str, new_last_page: int):
        async with self.async_session() as session:
            session: AsyncSession

            try:
                query = update(Book).filter_by(user_book=username, book_name=book_name).values(last_page=new_last_page)

                await session.execute(query)
                await session.commit()

            except Exception:
                return False

            else:
                return True

    async def delete_user_book(self, username: str, book_name: str):
        async with self.async_session() as session:
            session: AsyncSession

            try:
                querys = [
                    delete(Book).filter_by(user_book=username, book_name=book_name),
                    delete(BookMark).filter_by(bookmark_for_book=book_name, user=username)
                ]

                for query in querys:
                    await session.execute(query)

                await session.commit()

            except Exception:
                return False

            else:
                return True

    async def delete_user_book_mark(self, username: str, bookmark_for_book: str, page: int):
        async with self.async_session() as session:
            session: AsyncSession

            try:
                query = delete(BookMark).filter_by(bookmark_for_book=bookmark_for_book, user=username, num_bookmark=page)

                await session.execute(query)
                await session.commit()

            except Exception:
                return False

            else:
                return True

    async def exists_user(self, username: str) -> bool:
        async with self.async_session() as session:
            session: AsyncSession

            query = select(User).filter_by(username=username)
            result = await session.execute(query)

            return bool(result.scalars().all())

    async def exists_book_user(self, username: str, book: str) -> bool:
        async with self.async_session() as session:
            session: AsyncSession

            query = select(Book).filter_by(user_book=username, book_name=book)
            result = await session.execute(query)

            return bool(result.scalars().all())

    async def exists_book_mark_user(self, username: str, book: str, num_bk: int) -> bool:
        async with self.async_session() as session:
            session: AsyncSession

            query = select(BookMark).filter_by(user=username, bookmark_for_book=book, num_bookmark=num_bk)
            result = await session.execute(query)

            return bool(result.scalars().all())

    async def get_continue_book(self, username: str) -> dict[str, str | int]:
        async with self.async_session() as session:
            session: AsyncSession

            query = select(Book).filter_by(user_book=username, continue_read=True)
            result = await session.execute(query)

            book_result = result.scalars().all()
            if not book_result:
                return

            book = book_result[0]

            return {
                'book_name': book.book_name,
                'content_book': book.content_book,
                'last_page': book.last_page
            }

__all__ = (
    'DataBaseRequests',
)
