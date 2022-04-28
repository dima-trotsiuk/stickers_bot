import action as action
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import ADMINSITE
from handlers.users.api import API
from keyboards.default.cancel import cancel_button
from keyboards.default.menu import default_menu
from keyboards.inline.edit_order.callback_datas import click_product_to_basket_button_callback
from keyboards.inline.edit_order.product_to_basket import click_product_to_basket_button
from keyboards.inline.edit_product_buttons.callback_datas import show_product_buttons_callback, \
    choice_user_callback
from keyboards.inline.edit_product_buttons.choice_user_button import choice_user
from keyboards.inline.edit_product_buttons.show_product_buttons import show_product_buttons
from loader import dp
from states.create_order.set_quantity_order import SetQuantityOrderState


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

# @dp.callback_query_handler(
#     show_product_buttons_callback.filter(type_command="show_product_for_order"))
# async def choice_user_callback(call: CallbackQuery, callback_data: dict):
#     """
#     Спрацьовує при натискуванні на конкретний пак
#     """
#     await call.answer(cache_time=1)
#
#     pk = callback_data.get('pk')
#     if pk == '0':
#         await call.message.answer("Чий склад? 😐",
#                                   reply_markup=await choice_user(type_command='choice_user_for_order'))
#         await call.message.delete()
#     else:
#         choice_user_call = callback_data.get('choice_user')
#         quantity = 0
#         await click_product_to_basket_button(message=call.message, choice_user=choice_user_call, pk=pk,
#                                              quantity=quantity)
#
#
# @dp.callback_query_handler(
#     click_product_to_basket_button_callback.filter(type_command="cl_pr_ord"))
# async def show_product_buttons_callback(call: CallbackQuery, callback_data: dict, state: FSMContext):
#     """
#     Спрацьовує при натискуванні на  '+' '-' або 'власне значення'
#     """
#     await call.answer(cache_time=1)
#     action = callback_data.get('action')
#     choice_user = callback_data.get('choice_user')
#     pk = callback_data.get('pk')
#     quantity = int(callback_data.get('quantity'))
#
#     flag = {'dima': 'quantity_dima', 'vlad': 'quantity_vlad'}
#     quantity_user = flag[choice_user]
#
#     # Дізнаємось, яку кількість стікерів віднімати і додавати
#     product = API().storage_product_info(pk)
#
#     quantity_in_pack = int(product['quantity_in_pack'])
#     max_quantity = int(product['storage_stickers'][quantity_user])
#
#     if quantity_in_pack % 25 == 0:
#         plus_minus_value = 25
#     else:
#         plus_minus_value = quantity_in_pack
#
#     if action == 'plus':
#         if quantity+plus_minus_value <= max_quantity:
#             quantity += plus_minus_value
#             await click_product_to_basket_button(message=call.message, choice_user=choice_user, pk=pk, update=True,
#                                                  quantity=quantity)
#         else:
#             await call.message.answer("На складі нема стільки 😢")
#     elif action == 'minus':
#         if quantity-plus_minus_value >= 0:
#             quantity -= plus_minus_value
#             await click_product_to_basket_button(message=call.message, choice_user=choice_user, pk=pk, update=True,
#                                                  quantity=quantity)
#         else:
#             await call.message.answer("ШО 😢")
#     elif action == 'another':
#         await state.update_data(choice_user=choice_user)
#         await state.update_data(pk=pk)
#         await state.update_data(message=call.message)
#         await SetQuantityOrderState.quantity.set()
#         return await call.message.answer("Кількість? 🥺", reply_markup=cancel_button)
#     elif action == 'close':
#         await call.message.delete()
#     elif action == 'add':
#         admin = ADMINSITE[f"{call.message.chat.id}"]
#         products = API().bag_products_get_post()
#
#         flag = True
#         for product in products:
#             if product["product"] == int(pk) and product["user"] == admin:
#                 flag = False
#                 await call.message.answer("Вже є в корзині 🧐")
#                 break
#
#         if flag:
#             user = {'dima': 1, 'vlad': 2}
#             user = user[choice_user]
#             json_post = {
#                 "product": pk,
#                 "bag": admin,
#                 "quantity": quantity,
#                 "user": user
#             }
#
#             response = API().bag_products_get_post(json_post)
#             print(response)
#             await call.message.answer("Додано в корзину")
#             await call.message.delete()
#
#
# @dp.message_handler(text="Отмена", state=SetQuantityOrderState.quantity)
# async def cancel(message: types.Message, state: FSMContext):
#     await message.answer("Хорошо :)", reply_markup=default_menu)
#     await state.finish()
#
#
# @dp.message_handler(state=SetQuantityOrderState.quantity)
# async def another(message: types.Message, state: FSMContext):
#     quantity = message.text
#
#     data = await state.get_data()
#     choice_user = data.get("choice_user")
#     pk = data.get("pk")
#     message = data.get("message")
#
#     flag = {'dima': 'quantity_dima', 'vlad': 'quantity_vlad'}
#     quantity_user = flag[choice_user]
#
#     product = API().storage_product_quantity(pk)
#
#     if quantity.isdigit():
#         await state.finish()
#         if 0 <= int(quantity) <= product[quantity_user]:
#             await state.update_data(quantity=quantity)
#             await message.answer("Готово 😎", reply_markup=default_menu)
#             await click_product_to_basket_button(message=message, choice_user=choice_user, pk=pk, update=True,
#                                                  quantity=quantity)
#         else:
#             await message.answer("На складі нема стільки 😢", reply_markup=default_menu)
#     else:
#         await message.answer(f"Введи ціле число 😏")
