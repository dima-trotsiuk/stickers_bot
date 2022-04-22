from aiogram.utils.callback_data import CallbackData

show_buttons_callback = CallbackData("show_buttons", "type_command", "action")
click_product_to_basket_button_callback = CallbackData("click_product_to_basket_button", "type_command", "action", "pk",
                                                       "choice_user")

# click_product_to_basket_button_callback = CallbackData("click_product_to_basket_button", "type_command", "action", "pk",
#                                                        "quantity",
#                                                        "choice_user")
