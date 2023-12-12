from aiogram import Bot, Dispatcher
from config.config_data import Config
from database.start import start_db
from handlears import commands_handlears, download_files_handlears, callbacks_handlears
from pathlib import Path

import asyncio
import logging

logger = logging.getLogger(__name__)

async def main():
    path_db = Path(__file__).parent / 'database' / 'db.sqlite3'

    if Config.tg_bot.bot_logs:
        logging.basicConfig(level=logging.INFO)

    if not path_db.exists():
        logger.info('Start database')
        await start_db()

    logger.info('Start bot')

    bot = Bot(token=Config.tg_bot.bot_token, parse_mode='HTML')
    dp = Dispatcher()

    dp.include_routers(
        commands_handlears.router,
        callbacks_handlears.router,
        download_files_handlears.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    wb_info = await bot.get_webhook_info()

    if wb_info.allowed_updates:
        await dp.start_polling(bot, allowed_updates=[])

    else:
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
