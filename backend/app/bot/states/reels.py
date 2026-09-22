from aiogram.fsm.state import State, StatesGroup


class ReelsStates(StatesGroup):
    waiting_for_amount = State()
