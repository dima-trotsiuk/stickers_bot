from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

default_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Склад Дімона"),
            KeyboardButton(text="Склад Владоса"),
            KeyboardButton(text="Фулл склад"),
        ],
        [
            KeyboardButton(text="Редагувати склад"),
            KeyboardButton(text="Управління замовленнями"),
            KeyboardButton(text="Кошик"),
        ],
        [
            KeyboardButton(text="Пошук по ТТН"),
            KeyboardButton(text="Статистика"),
        ],
    ],
    resize_keyboard=True
)
