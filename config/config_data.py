from dotenv import load_dotenv
from os import getenv
from dataclasses import dataclass

load_dotenv()

@dataclass
class TelegramBot:
    bot_token: str
    bot_logs: bool

@dataclass
class DataBase:
    sql_alchemy_url: str
    db_logs: bool

@dataclass
class ConfigData:
    tg_bot: TelegramBot
    database: DataBase

def _get_a_choice_of_parameter(parametr: str) -> bool:
    menu = getenv(parametr.strip().upper()).upper()
    menu_choose = menu if menu in ('YES', 'NO') else 'NO'

    match menu_choose:

        case "YES":
            return True

        case "NO":
            return False

def _load_config_data() -> ConfigData:
    return ConfigData(
        tg_bot=TelegramBot(
            bot_token=getenv('BOT_TOKEN'),
            bot_logs=_get_a_choice_of_parameter(parametr='BOT_LOGS')
        ),
        database=DataBase(
            sql_alchemy_url=getenv('SQLALCHEMY_URL'),
            db_logs=_get_a_choice_of_parameter(parametr='DATABASE_LOGS')
        )
    )

Config = _load_config_data()

__all__ = (
    'Config',
)
