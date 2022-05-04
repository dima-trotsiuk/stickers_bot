from aiogram.dispatcher.filters.state import StatesGroup, State


class GetTtnState(StatesGroup):
    ttn = State()
