from aiogram import types

from keyboards.inline.edit_order.show_buttons import show_buttons_order
from loader import dp


@dp.message_handler(text="Управління замовленнями")
async def get_storage_dima_vlad(message: types.Message):
    await message.answer("Кайфарік 🤩", reply_markup=await show_buttons_order())



