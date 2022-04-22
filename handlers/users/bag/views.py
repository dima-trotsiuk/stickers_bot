from aiogram import types

from keyboards.inline.bag.show_buttons_products import show_buttons_products_bag
from keyboards.inline.edit_product_buttons.choice_user_button import choice_user
from loader import dp


@dp.message_handler(text="Кошик")
async def get_storage_dima_vlad(message: types.Message):
    await message.answer("Кошик", reply_markup=await show_buttons_products_bag(message))
