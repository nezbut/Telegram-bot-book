from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from lexicon.lexicon_ru import LEXICON_KEYBOARDS

def get_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(
            text=text
        ) for text in LEXICON_KEYBOARDS['main_keyboard'].values()
    ]

    builder.add(*buttons)
    builder.adjust(1, 2, 1)

    return builder.as_markup(resize_keyboard=True)

__all__ = (
    'get_main_keyboard',
)
