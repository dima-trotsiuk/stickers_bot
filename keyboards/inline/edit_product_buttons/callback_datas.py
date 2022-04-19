from aiogram.utils.callback_data import CallbackData

choice_user_callback = CallbackData("user", "type_command", "choice_user")
show_product_buttons_callback = CallbackData("show_product_buttons", "type_command", "pk", "choice_user")
click_product_button_callback = CallbackData("click_product_button", "type_command", "action", "pk", "choice_user")
