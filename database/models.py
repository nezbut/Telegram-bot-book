from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from config.config_data import Config

EngineDB = create_async_engine(Config.database.sql_alchemy_url, echo=Config.database.db_logs)

class Base(DeclarativeBase):
    pass

def get_session() -> AsyncSession:
    return async_sessionmaker(EngineDB)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(256), unique=True)

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    book_name = Column(String(256), unique=True)
    content_book = Column(Text)
    last_page = Column(Integer, default=1)
    continue_read = Column(Boolean, default=False)
    user_book = Column(String(256), ForeignKey('users.username', ondelete='CASCADE'))

class BookMark(Base):
    __tablename__ = "books_marks"

    id = Column(Integer, primary_key=True)
    bookmark_for_book = Column(String(256), ForeignKey('books.book_name', ondelete='CASCADE'))
    user = Column(String(256), ForeignKey('users.username', ondelete='CASCADE'))
    num_bookmark = Column(Integer)


__all__ = (
    'EngineDB',
    'Base',
    'get_session',
    'User',
    'Book',
    'BookMark'
)
