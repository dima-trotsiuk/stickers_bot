from aiogram.types import CallbackQuery

from handlers.users.api import API
from handlers.users.order_management.view_call import view_orders_is_processing
from keyboards.inline.edit_order.callback_datas import show_buttons_callback
from keyboards.inline.edit_product_buttons.choice_user_button import choice_user
from loader import dp


@dp.callback_query_handler(
    show_buttons_callback.filter(type_command="show_buttons_order"))
async def choice_user_callback(call: CallbackQuery, callback_data: dict):
    await call.answer()
    action = callback_data.get('action')

    if action == 'create':
        await call.message.answer("Чий склад? 😐", reply_markup=await choice_user(type_command='choice_user_for_order'))

    elif action == 'view':
        await view_orders_is_processing(call.message)
    elif action == 'send':
        updated = API().processing_to_done()['updated']
        if updated == '0':
            await call.message.answer(f"Нема шо відправляти 🧐")
        else:
            await call.message.answer(f"Відправлено ({updated})")
