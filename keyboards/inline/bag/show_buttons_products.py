from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.config import ADMINSITE
from handlers.users.api import API
from keyboards.inline.bag.callback_datas import show_buttons_products_bag_callback


async def show_buttons_products_bag(message):
    admin = ADMINSITE[f"{message.chat.id}"]

    bag_plus_products = API().bag_plus_product_get_update(pk=admin)

    bag_products = bag_plus_products['bag_products']

    list_button = []
    for bag_product in bag_products:
        pk = bag_product['pk']
        product_id = bag_product['product']
        quantity = bag_product['quantity']

        storage_product = API().storage_product_info(product_id)
        title = storage_product['title']

        el = [
            InlineKeyboardButton(
                text=f'"{title}" - {quantity}шт',
                callback_data=show_buttons_products_bag_callback.new(type_command="bag_click_pr", product_in_bag_pk=pk)
            ),
        ]
        list_button.append(el)
    el = [
        InlineKeyboardButton(
            text=f'Замовлення готове 🤝',
            callback_data=show_buttons_products_bag_callback.new(type_command="bag_click_pr",
                                                                 product_in_bag_pk="ready")
        ),
    ]
    list_button.append(el)
    return InlineKeyboardMarkup(row_width=1, inline_keyboard=list_button)
