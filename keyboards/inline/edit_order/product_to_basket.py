from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.config import ADMINSITE
from handlers.users.api import API
from .callback_datas import click_product_to_basket_button_callback


async def click_product_to_basket_button(message, choice_user, pk):
    products_in_bag = API().bag_products_get_post()
    product = API().storage_product_info(pk)

    flag = {'dima': 'quantity_dima', 'vlad': 'quantity_vlad'}

    quantity_user = flag[choice_user]
    choice_user_id = {'dima': 1, 'vlad': 2}
    choice_user_id = choice_user_id[choice_user]
    quantity = product['storage_stickers'][quantity_user]

    admin = ADMINSITE[f"{message.chat.id}"]
    flag = True
    for product_in_bag in products_in_bag:
        if product_in_bag["product"] == int(pk) and product_in_bag["bag"] == admin and product_in_bag["user"] == choice_user_id:
            flag = False
            break
    if flag:
        list_button = [
            [
                InlineKeyboardButton(
                    text="Додати в корзину",
                    callback_data=click_product_to_basket_button_callback.new(action="add",
                                                                              type_command=f'clk_prt_order',
                                                                              pk=pk,
                                                                              choice_user=choice_user)
                ),
            ],

        ]
    else:
        list_button = [
            [
                InlineKeyboardButton(
                    text="Вже в корзині, дядь 😩",
                    callback_data=click_product_to_basket_button_callback.new(action="empty",
                                                                              type_command=f'clk_prt_order',
                                                                              pk=pk,
                                                                              choice_user=choice_user)
                ),
            ],

        ]
    list_button.append([
        InlineKeyboardButton(
            text="Закрити",
            callback_data=click_product_to_basket_button_callback.new(action="close",
                                                                      type_command=f'clk_prt_order',
                                                                      pk=pk,
                                                                      choice_user=choice_user)
        ),
    ])
    button = InlineKeyboardMarkup(row_width=1, inline_keyboard=list_button)
    await message.answer(f"'{product['title']}' - {quantity}шт", reply_markup=button)

# async def click_product_to_basket_button(message, choice_user, pk, quantity, update=False):
#     product = API().storage_product_info(pk)
#
#     quantity_in_pack = int(product['quantity_in_pack'])
#
#     pk = product['pk']
#     if quantity_in_pack % 25 == 0:
#         plus_minus_value = 25
#     else:
#         plus_minus_value = quantity_in_pack
#     list_button = [
#         [
#             InlineKeyboardButton(
#                 text=f"-{plus_minus_value}",
#                 callback_data=click_product_to_basket_button_callback.new(action="minus",
#                                                                           type_command=f'cl_pr_ord',
#                                                                           pk=pk,
#                                                                           quantity=quantity,
#                                                                           choice_user=choice_user)
#             ),
#             InlineKeyboardButton(
#                 text=f"Власне значення 🥺",
#                 callback_data=click_product_to_basket_button_callback.new(action="another",
#                                                                           type_command=f'cl_pr_ord',
#                                                                           pk=pk,
#                                                                           quantity=quantity,
#                                                                           choice_user=choice_user)
#             ),
#             InlineKeyboardButton(
#                 text=f"+{plus_minus_value}",
#                 callback_data=click_product_to_basket_button_callback.new(action="plus",
#                                                                           type_command=f'cl_pr_ord',
#                                                                           pk=pk,
#                                                                           quantity=quantity,
#                                                                           choice_user=choice_user)
#             )
#         ],
#         [
#             InlineKeyboardButton(
#                 text="Додати в корзину",
#                 callback_data=click_product_to_basket_button_callback.new(action="add",
#                                                                           type_command=f'cl_pr_ord',
#                                                                           pk=pk,
#                                                                           quantity=quantity,
#                                                                           choice_user=choice_user)
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 text="Закрити",
#                 callback_data=click_product_to_basket_button_callback.new(action="close",
#                                                                           type_command=f'cl_pr_ord',
#                                                                           pk=pk,
#                                                                           quantity=quantity,
#                                                                           choice_user=choice_user)
#             ),
#         ]
#     ]
#     button = InlineKeyboardMarkup(row_width=1, inline_keyboard=list_button)
#     if update:
#         await bot.edit_message_text(chat_id=message.chat.id,
#                                     message_id=message.message_id,
#                                     text=f"'{product['title']}' - {quantity}шт", reply_markup=button)
#     else:
#         await message.answer(f"'{product['title']}' - {quantity}шт", reply_markup=button)
