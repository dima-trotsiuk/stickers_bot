from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from handlers.users.api import API
from keyboards.inline.bag.callback_datas import edit_quantity_bag_callback
from loader import bot


async def edit_quantity_bag(message, pk, update=False):
    product_bag = API().bag_product_get_update(pk)

    product_id = product_bag['product']
    quantity = product_bag['quantity']

    storage_product = API().storage_product_info(product_id)

    quantity_in_pack = int(storage_product['quantity_in_pack'])

    if quantity_in_pack % 25 == 0:
        plus_minus_value = 25
    else:
        plus_minus_value = quantity_in_pack
    list_button = [
        [
            InlineKeyboardButton(
                text=f"-{plus_minus_value}",
                callback_data=edit_quantity_bag_callback.new(action="minus",
                                                             type_command=f'edit_pr_bag',
                                                             product_in_bag_pk=pk)
            ),
            InlineKeyboardButton(
                text=f"Власне значення 🥺",
                callback_data=edit_quantity_bag_callback.new(action="another",
                                                             type_command=f'edit_pr_bag',
                                                             product_in_bag_pk=pk)
            ),
            InlineKeyboardButton(
                text=f"+{plus_minus_value}",
                callback_data=edit_quantity_bag_callback.new(action="plus",
                                                             type_command=f'edit_pr_bag',
                                                             product_in_bag_pk=pk)
            )
        ],
        [
            InlineKeyboardButton(
                text="Закрити",
                callback_data=edit_quantity_bag_callback.new(action="close",
                                                             type_command=f'edit_pr_bag',
                                                             product_in_bag_pk=pk)
            ),
        ]
    ]
    button = InlineKeyboardMarkup(row_width=1, inline_keyboard=list_button)
    if update:
        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=message.message_id,
                                    text=f"'{storage_product['title']}' - {quantity}шт", reply_markup=button)
    else:
        await message.answer(f"'{storage_product['title']}' - {quantity}шт", reply_markup=button)
