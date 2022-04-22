from aiogram.types import CallbackQuery

from handlers.users.api import API
from keyboards.inline.bag.show_buttons_products import show_buttons_products_bag
from keyboards.inline.bag.callback_datas import edit_quantity_bag_callback
from keyboards.inline.bag.edit_quantity_bag import edit_quantity_bag
from loader import dp


@dp.callback_query_handler(
    edit_quantity_bag_callback.filter(type_command="edit_pr_bag"))
async def edit_quantity_call(call: CallbackQuery, callback_data: dict):
    """
    Ця функція реагує на клік по товару в корзині
    """
    await call.answer(cache_time=1)

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
                await patch(quantity, product_in_bag_pk, call.message)
            else:
                await call.message.answer("На складі нема стільки 😢")
        else:
            if quantity - plus_minus_value >= 0:
                quantity -= plus_minus_value
                await patch(quantity, product_in_bag_pk, call.message)
            else:
                await call.message.answer("ШО 😢")
    elif action == 'close':

        await call.message.delete()
        await call.message.answer("Кошик", reply_markup=await show_buttons_products_bag(call.message))


async def patch(quantity, product_in_bag_pk, message):
    json_patch = {
        "quantity": quantity,
    }
    API().bag_product_get_update(pk=product_in_bag_pk, json_patch=json_patch)
    await edit_quantity_bag(message=message, pk=product_in_bag_pk, update=True)