from aiogram import types

from keyboards.inline.edit_product_buttons.choice_user_button import choice_user
from loader import dp


@dp.message_handler(text="Редагувати склад")
async def get_storage_dima_vlad(message: types.Message):
    await message.answer("Давай, давай 😐", reply_markup=await choice_user())



