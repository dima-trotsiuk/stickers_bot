from aiogram import types

from handlers.users.api import API
from loader import dp


@dp.message_handler(text=["Склад Дімона", "Склад Владоса"])
async def get_storage_dima_vlad(message: types.Message):
    product_info_list = API().storage_products_info()

    flag = {'Склад Дімона': 'quantity_dima', 'Склад Владоса': 'quantity_vlad'}
    user = flag[message.text]

    if message.text == 'Склад Дімона':
        text = 'Склад Дмутра ☺️\n\n'
    else:
        text = 'Склад Владоса ☺️\n\n'

    for product_info in product_info_list:
        text += f"<i>'{product_info['title']}'</i> - "
        text += f"<b>{product_info['storage_stickers'][user]}</b>шт\n"
    await message.answer(text)


@dp.message_handler(text="Фулл склад")
async def get_storage_full(message: types.Message):
    product_info_list = API().storage_products_info()

    text = 'Фулл склад 😓️\n\n'

    for product_info in product_info_list:
        text += f"<i>'{product_info['title']}'</i> - "
        text += f"<b>{product_info['total_quantity']}</b>шт\n"
    await message.answer(text)