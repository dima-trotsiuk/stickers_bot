from aiogram.types import CallbackQuery

from keyboards.inline.bag.callback_datas import show_buttons_products_bag_callback
from keyboards.inline.bag.edit_quantity_bag import edit_quantity_bag
from loader import dp


@dp.callback_query_handler(
    show_buttons_products_bag_callback.filter(type_command="bag_click_pr"))
async def show_buttons_products_bag(call: CallbackQuery, callback_data: dict):
    """
    Ця функція реагує на команди зміни кількості товару в корзині
    """
    await call.answer(cache_time=1)
    product_in_bag_pk = callback_data.get('product_in_bag_pk')

    await edit_quantity_bag(message=call.message, pk=product_in_bag_pk)
    await call.message.delete()




