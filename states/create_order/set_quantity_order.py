from aiogram.dispatcher.filters.state import StatesGroup, State


class SetQuantityOrderState(StatesGroup):
    quantity = State()
