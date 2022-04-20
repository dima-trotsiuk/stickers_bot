from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from handlers.users.api import API
from .callback_datas import show_product_buttons_callback


async def show_product_buttons(choice_user):
    product_info_list = API().storage_products_info()

    list_button = []

    flag = {'dima': 'quantity_dima', 'vlad': 'quantity_vlad'}

    for product in product_info_list:
        title = product['title']
        pk = product['pk']
        quantity = product['storage_stickers'][flag[choice_user]]

        el = [
            InlineKeyboardButton(
                text=f'"{title}" - {quantity}шт',
                callback_data=show_product_buttons_callback.new(type_command=f'show_product',
                                                                pk=pk,
                                                                choice_user=choice_user)
            ),
        ]
        list_button.append(el)

    return InlineKeyboardMarkup(row_width=1, inline_keyboard=list_button)
