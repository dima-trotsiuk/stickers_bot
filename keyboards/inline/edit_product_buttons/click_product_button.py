from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from handlers.users.api import API
from loader import bot
from .callback_datas import click_product_button_callback


async def click_product_button(message, choice_user, pk, update=False):
    product = API().storage_product_info(pk)

    flag = {'dima': 'quantity_dima', 'vlad': 'quantity_vlad'}
    quantity_user = flag[choice_user]

    quantity_in_pack = int(product['quantity_in_pack'])

    quantity = product['storage_stickers'][quantity_user]
    pk = product['pk']
    if quantity_in_pack % 25 == 0:
        plus_minus_value = 25
    else:
        plus_minus_value = quantity_in_pack
    list_button = [
        [
            InlineKeyboardButton(
                text=f"-{plus_minus_value}",
                callback_data=click_product_button_callback.new(action="minus",
                                                                type_command=f'click_product',
                                                                pk=pk,
                                                                choice_user=choice_user)
            ),
            InlineKeyboardButton(
                text=f"Власне значення 🥺",
                callback_data=click_product_button_callback.new(action="another",
                                                                type_command=f'click_product',
                                                                pk=pk,
                                                                choice_user=choice_user)
            ),
            InlineKeyboardButton(
                text=f"+{plus_minus_value}",
                callback_data=click_product_button_callback.new(action="plus",
                                                                type_command=f'click_product',
                                                                pk=pk,
                                                                choice_user=choice_user)
            )
        ],
        [
        InlineKeyboardButton(
            text="Закрити",
            callback_data=click_product_button_callback.new(action="close",
                                                            type_command=f'click_product',
                                                            pk=pk,
                                                            choice_user=choice_user)
        ),
        ]
    ]
    button = InlineKeyboardMarkup(row_width=1, inline_keyboard=list_button)
    if update:
        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=message.message_id,
                                    text=f"'{product['title']}' - {quantity}шт", reply_markup=button)
    else:
        await message.answer(f"'{product['title']}' - {quantity}шт", reply_markup=button)
