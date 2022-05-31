from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.users.api import API
from keyboards.default.cancel import cancel_button
from keyboards.default.menu import default_menu
from keyboards.inline.bag.show_buttons_products import show_buttons_products_bag
from keyboards.inline.bag.callback_datas import edit_quantity_bag_callback
from keyboards.inline.bag.edit_quantity_bag import edit_quantity_bag
from loader import dp
from states.edit_product.set_quantity import SetQuantityState2


@dp.callback_query_handler(
    edit_quantity_bag_callback.filter(type_command="edit_pr_bag"))
async def edit_quantity_call(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Ця функція реагує на клік по товару в корзині
    """

    action = callback_data.get('action')
    product_in_bag_pk = callback_data.get('product_in_bag_pk')

    product_bag = API().bag_product_get_update(product_in_bag_pk)

    product_id = product_bag['product']
    quantity = product_bag['quantity']
    user = product_bag['user']

    storage_product = API().storage_product_info(product_id)

    flag = {1: 'quantity_dima', 2: 'quantity_vlad'}
    quantity_user = flag[user]

    quantity_in_pack = storage_product['quantity_in_pack']
    max_quantity = int(storage_product['storage_stickers'][quantity_user])

    if quantity_in_pack % 25 == 0:
        plus_minus_value = 25
    else:
        plus_minus_value = quantity_in_pack

    if action in ['plus', 'minus']:
        if action == 'plus':
            if quantity + plus_minus_value <= max_quantity:
                quantity += plus_minus_value
                await patch(quantity, product_in_bag_pk)
                await edit_quantity_bag(message=call.message, pk=product_in_bag_pk, update=True)
            else:
                await call.message.answer("На складі нема стільки 😢")
        else:
            if quantity - plus_minus_value >= 0:
                quantity -= plus_minus_value
                await patch(quantity, product_in_bag_pk)
                await edit_quantity_bag(message=call.message, pk=product_in_bag_pk, update=True)
            else:
                await call.message.answer("ШО 😢")
    elif action == 'close':
        await call.message.delete()
        await show_buttons_products_bag(call.message)
    elif action == 'another':
        await call.message.delete()
        await call.message.answer('Введи значення:', reply_markup=cancel_button)
        await state.update_data(product_in_bag_pk=product_in_bag_pk)
        await SetQuantityState2.quantity.set()


@dp.message_handler(text="Отмена", state=SetQuantityState2.quantity)
async def share_number_func(message: types.Message, state: FSMContext):
    await message.answer("Хорошо :)", reply_markup=default_menu)
    await state.finish()


@dp.message_handler(state=SetQuantityState2.quantity)
async def answer_another(message: types.Message, state: FSMContext):

    data = await state.get_data()
    product_in_bag_pk = data.get("product_in_bag_pk")

    quantity_user = message.text

    if quantity_user.isdigit():
        await state.finish()
        quantity_user = int(quantity_user)

        product_bag = API().bag_product_get_update(product_in_bag_pk)

        product_id = product_bag['product']
        user = product_bag['user']

        flag = {1: 'quantity_dima', 2: 'quantity_vlad'}
        quantity_user_flag = flag[user]

        storage_product = API().storage_product_info(product_id)
        max_quantity = int(storage_product['storage_stickers'][quantity_user_flag])

        if 0 < quantity_user <= max_quantity:
            quantity_stickers = quantity_user
            await message.reply(f"Готово 🛒", reply_markup=default_menu)
            await patch(quantity_stickers, product_in_bag_pk)
            await show_buttons_products_bag(message)
        else:
            await message.reply(f"На складе є тільки {max_quantity}шт 😥", reply_markup=default_menu)
    else:
        await message.answer(f"Введи ціле  число!")


async def patch(quantity, product_in_bag_pk):
    json_patch = {
        "quantity": quantity,
    }
    API().bag_product_get_update(pk=product_in_bag_pk, json_patch=json_patch)
