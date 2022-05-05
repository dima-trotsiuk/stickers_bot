from aiogram.types import CallbackQuery

from data.config import ADMINSITE
from handlers.users.api import API
from keyboards.inline.edit_order.callback_datas import click_product_to_basket_button_callback
from keyboards.inline.edit_order.product_to_basket import click_product_to_basket_button
from keyboards.inline.edit_product_buttons.callback_datas import show_product_buttons_callback, \
    choice_user_callback
from keyboards.inline.edit_product_buttons.choice_user_button import choice_user
from keyboards.inline.edit_product_buttons.show_product_buttons import show_product_buttons
from loader import dp


@dp.callback_query_handler(
    choice_user_callback.filter(type_command="choice_user_for_order"))
async def choice_user_for_order_callback(call: CallbackQuery, callback_data: dict):
    """
    Ця функція реагує на кнопки вибору користувача, чий склад буде редагуватись
    """
    await call.answer(cache_time=1)

    user = callback_data.get('choice_user')

    await call.message.answer('Додай товари до замовлення 😜',
                              reply_markup=await show_product_buttons(choice_user=user,
                                                                      type_command='show_product_for_order'))
    await call.message.delete()


@dp.callback_query_handler(
    show_product_buttons_callback.filter(type_command="show_product_for_order"))
async def show_product_for_order_callback(call: CallbackQuery, callback_data: dict):
    """
    Спрацьовує при натискуванні на конкретний пак
    """
    await call.answer(cache_time=1)
    pk = callback_data.get('pk')
    if pk == '0':
        await call.message.answer("Чий склад? 😐",
                                  reply_markup=await choice_user(type_command='choice_user_for_order'))
        await call.message.delete()
    else:
        choice_user_call = callback_data.get('choice_user')
        await click_product_to_basket_button(message=call.message,
                                             choice_user=choice_user_call,
                                             pk=pk)


@dp.callback_query_handler(
    click_product_to_basket_button_callback.filter(type_command="clk_prt_order"))
async def show_product_buttons_callback(call: CallbackQuery, callback_data: dict):
    """
    Спрацьовує при натискуванні на  'Додати в корзину' 'Закрити' або 'власне значення'
    """
    await call.answer(cache_time=1)

    choice_user = callback_data.get('choice_user')
    pk = callback_data.get('pk')
    action = callback_data.get('action')
    admin = ADMINSITE[f"{call.message.chat.id}"]

    if action == 'add':
        user = {'dima': 1, 'vlad': 2}
        user = user[choice_user]
        json_post = {
            "product": pk,
            "bag": admin,
            "user": user
        }

        API().bag_products_get_post(json_post)
        await call.message.answer("Додано в корзину")
        await call.message.delete()
    elif action == 'close':
        await call.message.delete()
