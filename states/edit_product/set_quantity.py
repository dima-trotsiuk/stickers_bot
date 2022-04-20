from aiogram.dispatcher.filters.state import StatesGroup, State


class SetQuantityState(StatesGroup):
    quantity = State()
