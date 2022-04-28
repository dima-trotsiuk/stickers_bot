import json

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import ADMINSITE
from handlers.users.api import API
from handlers.users.order_management.view_call import print_order
from keyboards.inline.bag.callback_datas import show_buttons_products_bag_callback
from keyboards.inline.bag.edit_quantity_bag import edit_quantity_bag
from loader import dp, bot
from states.order_is_ready.order_is_ready_state import OrderIsReadyState


@dp.callback_query_handler(
    show_buttons_products_bag_callback.filter(type_command="bag_click_pr"))
async def show_buttons_products_bag(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Ця функція реагує на команди зміни кількості товару в корзині
    """
    await call.answer(cache_time=1)
    product_in_bag_pk = callback_data.get('product_in_bag_pk')

    # перевіряємо, чи була натиснута кнопка "замовлення готове"
    if product_in_bag_pk == 'ready':
        await OrderIsReadyState.ttn.set()
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer("Введи ТТН:")
    else:
        await edit_quantity_bag(message=call.message, pk=product_in_bag_pk)
        await call.message.delete()


"""
Реалізовуємо state
"""


@dp.message_handler(state=OrderIsReadyState.ttn)
async def answer_q1(message: types.Message, state: FSMContext):
    ttn = message.text
    json_patch = {
        "ttn": ttn,
    }
    bag_id = ADMINSITE[f"{message.chat.id}"]
    API().bag_detail_get_update(bag_id, json_patch)

    await message.answer("Введи суму:")
    await OrderIsReadyState.price.set()


@dp.message_handler(state=OrderIsReadyState.price)
async def answer_q2(message: types.Message, state: FSMContext):
    price = message.text
    if price.isdigit():
        json_patch = {
            "price": price,
        }
        bag_id = ADMINSITE[f"{message.chat.id}"]
        API().bag_detail_get_update(bag_id, json_patch)

        response = API().bag_create(1)

        if response.status_code == 409:
            await message.answer("Сталась помилка при створенні замовлення. Попробуй звірити кількість товару.")
        else:
            response = json.loads(response.text)
            order_info = API().order_get(response['pk_order'])
            await message.answer(print_order(order_info))

        await state.finish()
    else:
        await message.answer("Введи ЧИСЛО:")
        await OrderIsReadyState.price.set()
