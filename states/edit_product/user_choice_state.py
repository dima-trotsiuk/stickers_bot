from aiogram.dispatcher.filters.state import StatesGroup, State


class UserChoiceState(StatesGroup):
    user = State()
