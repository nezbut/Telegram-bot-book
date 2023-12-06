from dotenv import load_dotenv
from os import getenv
from dataclasses import dataclass

load_dotenv()

@dataclass
class TelegramBot:
    bot_token: str

@dataclass
class DataBase:
    sql_alchemy_url: str

@dataclass
class ConfigData:
    tg_bot: TelegramBot
    database: DataBase

def load_config_data() -> ConfigData:
    return ConfigData(
        tg_bot=TelegramBot(
            bot_token=getenv('BOT_TOKEN')
        ),
        database=DataBase(
            sql_alchemy_url=getenv('SQLALCHEMY_URL')
        )
    )

Config = load_config_data()

__all__ = (
    'Config',
)
