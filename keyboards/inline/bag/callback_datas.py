from aiogram.utils.callback_data import CallbackData

show_buttons_products_bag_callback = CallbackData("show_buttons_products_bag", "type_command", "product_in_bag_pk")
edit_quantity_bag_callback = CallbackData("edit_quantity_bag", "type_command", "action", "product_in_bag_pk")
