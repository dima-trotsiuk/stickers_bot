from aiogram.dispatcher.filters.state import StatesGroup, State


class OrderIsReadyState(StatesGroup):
    ttn = State()
    price = State()
