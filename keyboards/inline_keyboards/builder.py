from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def inline_keyboard_builder(
        width: int,
        *args: str,
        callback_and_text_dict: dict[str, str] | None = None,
        last_buttons: list[str] | dict[str, str] | None = None
    ) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            buttons.append(
                InlineKeyboardButton(
                    text=button,
                    callback_data=button
                )
            )

    if callback_and_text_dict:
        for callback_data, text in callback_and_text_dict.items():
            buttons.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=callback_data
                )
            )

    builder.row(*buttons, width=width)

    if last_buttons:
        map_obj = None

        if isinstance(last_buttons, list):
            map_obj = map(lambda text: InlineKeyboardButton(text=text, callback_data=text), last_buttons)

        elif isinstance(last_buttons, dict):
            map_obj = map(lambda tuple_button: InlineKeyboardButton(text=tuple_button[-1], callback_data=tuple_button[0]), last_buttons.items())

        builder.row(*map_obj, width=2)

    return builder.as_markup()

__all__ = (
    'inline_keyboard_builder',
)
