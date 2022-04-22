from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callback_datas import choice_user_callback


async def choice_user(type_command='choice_user'):
    list_button = [
        [
            InlineKeyboardButton(
                text=f"Дімона",
                callback_data=choice_user_callback.new(choice_user="dima", type_command=type_command)
            ),
            InlineKeyboardButton(
                text=f"Владоса",
                callback_data=choice_user_callback.new(choice_user="vlad", type_command=type_command)
            )
        ]
    ]

    return InlineKeyboardMarkup(row_width=1, inline_keyboard=list_button)
