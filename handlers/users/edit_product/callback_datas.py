import json

import requests
from aiogram.types import CallbackQuery

from data.config import BASE_URL
from keyboards.inline.edit_product_buttons.callback_datas import choice_user_callback, show_product_buttons_callback, \
    click_product_button_callback
from keyboards.inline.edit_product_buttons.click_product_button import click_product_button
from keyboards.inline.edit_product_buttons.show_product_buttons import show_product_buttons

from loader import dp


@dp.callback_query_handler(
    choice_user_callback.filter(type_command="choice_user"))
async def choice_user_callback(call: CallbackQuery, callback_data: dict):
    """
    Ця функція реагує на кнопки вибору користувача, чий склад буде редагуватись
    """
    await call.answer()
    user = callback_data.get('choice_user')

    await call.message.answer("Складік 🤩", reply_markup=await show_product_buttons(user))


@dp.callback_query_handler(
    show_product_buttons_callback.filter(type_command="show_product"))
async def show_product_buttons_callback(call: CallbackQuery, callback_data: dict):
    """
    Спрацьовує при натискуванні на зміну конкретного стікерпаку
    """
    await call.answer()
    user = callback_data.get('choice_user')
    pk = callback_data.get('pk')

    await click_product_button(message=call.message, choice_user=user, pk=pk)


@dp.callback_query_handler(
    click_product_button_callback.filter(type_command="click_product"))
async def show_product_buttons_callback(call: CallbackQuery, callback_data: dict):
    """
    Спрацьовує при натискуванні на  '+' '-' або 'власне значення'
    """
    await call.answer()
    action = callback_data.get('action')
    choice_user = callback_data.get('choice_user')
    pk = callback_data.get('pk')

    flag = {'dima': 'quantity_dima', 'vlad': 'quantity_vlad'}
    quantity_user = flag[choice_user]

    # Дізнаємось, яку кількість стікерів віднімати і додавати
    product = requests.get(f'{BASE_URL}/v1/product_info/{pk}/')
    product = json.loads(product.text)

    quantity_in_pack = int(product['quantity_in_pack'])
    quantity = int(product['storage_stickers'][quantity_user])

    if quantity_in_pack % 25 == 0:
        plus_minus_value = 25
    else:
        plus_minus_value = quantity_in_pack

    if action == 'plus':
        quantity += plus_minus_value
    elif action == 'minus':
        quantity -= plus_minus_value

    # Оновлюємо дані в БД
    updated_product = {
        f"{quantity_user}": quantity
    }

    response = requests.patch(f'{BASE_URL}/v1/product_quantity/{pk}/', json=updated_product)

    await click_product_button(message=call.message, choice_user=choice_user, pk=pk, update=True)
