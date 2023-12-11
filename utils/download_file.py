from aiogram import Bot

async def get_book_content_in_txt_file(bot: Bot, txt_file_id: str) -> str:
    file = await bot.get_file(file_id=txt_file_id)
    download_file = await bot.download_file(file_path=file.file_path)

    cont = download_file.read().decode()

    book_content = " ".join(cont.split()).strip()
    return book_content

__all__ = (
    'get_book_content_in_txt_file',
)
