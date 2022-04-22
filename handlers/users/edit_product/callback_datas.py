from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from handlers.users.api import API
from keyboards.default.cancel import cancel_button
from keyboards.default.menu import default_menu
from keyboards.inline.edit_product_buttons.callback_datas import choice_user_callback, show_product_buttons_callback, \
    click_product_button_callback
from keyboards.inline.edit_product_buttons.click_product_button import click_product_button
from keyboards.inline.edit_product_buttons.show_product_buttons import show_product_buttons

from loader import dp
from states.edit_product.set_quantity import SetQuantityState


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
async def show_product_buttons_callback(call: CallbackQuery, callback_data: dict, state: FSMContext):
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
    product = API().storage_product_info(pk)

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
    elif action == 'another':
        await state.update_data(choice_user=choice_user)
        await state.update_data(pk=pk)
        await state.update_data(message=call.message)
        await SetQuantityState.quantity.set()
        await call.message.delete()
        return await call.message.answer("Кількість? 🥺", reply_markup=cancel_button)
    elif action == 'close':
        await call.message.delete()
        return True

    # Оновлюємо дані в БД
    updated_product = {
        f"{quantity_user}": quantity
    }

    API().storage_product_quantity_update(pk, updated_product)

    await click_product_button(message=call.message, choice_user=choice_user, pk=pk, update=True)


@dp.message_handler(text="Отмена", state=SetQuantityState.quantity)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Хорошо :)", reply_markup=default_menu)
    await state.finish()


@dp.message_handler(state=SetQuantityState.quantity)
async def another(message: types.Message, state: FSMContext):
    quantity = message.text

    data = await state.get_data()
    choice_user = data.get("choice_user")
    flag = {'dima': 'quantity_dima', 'vlad': 'quantity_vlad'}

    quantity_user = flag[choice_user]
    pk = data.get("pk")
    message = data.get("message")

    if quantity.isdigit():
        await state.finish()
        if int(quantity) >= 0:

            updated_product = {
                f"{quantity_user}": quantity
            }

            API().storage_product_quantity_update(pk, updated_product)
            await message.answer("Готово 😎", reply_markup=default_menu)
    else:
        await message.answer(f"Введи ціле число 😏")