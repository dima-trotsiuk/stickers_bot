from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.api import API
from handlers.users.order_management.view_call import print_order
from loader import dp
from states.search_for_ttn.get_ttn import GetTtnState


@dp.message_handler(text="Пошук по ТТН")
async def get_storage_dima_vlad(message: types.Message):
    await message.answer(f"Введи ТТН:")
    await GetTtnState.ttn.set()


@dp.message_handler(state=GetTtnState.ttn)
async def answer_q2(message: types.Message, state: FSMContext):
    ttn = message.text
    orders = API().search_for_ttn_get(ttn)
    if orders == 404:
        await message.answer('Не знайдено 🧐')
    else:
        for order in orders:
            await message.answer(print_order(order))
    await state.finish()
