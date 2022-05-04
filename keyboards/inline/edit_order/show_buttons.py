from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callback_datas import show_buttons_callback


async def show_buttons_order():
    list_button = [
        [
            InlineKeyboardButton(
                text=f"Створити",
                callback_data=show_buttons_callback.new(action="create", type_command='show_buttons_order')
            ),
            InlineKeyboardButton(
                text=f"Переглянути",
                callback_data=show_buttons_callback.new(action="view", type_command='show_buttons_order')
            ),
            InlineKeyboardButton(
                text=f"Відправити",
                callback_data=show_buttons_callback.new(action="send", type_command='show_buttons_order')
            ),
        ],

    ]

    return InlineKeyboardMarkup(row_width=1, inline_keyboard=list_button)
