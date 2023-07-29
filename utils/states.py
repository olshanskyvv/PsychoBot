from aiogram.fsm.state import StatesGroup, State


class PrimaryRecord(StatesGroup):
    choosing_date = State()
    choosing_time = State()
    confirm = State()


class SecondaryRecord(StatesGroup):
    choosing_service = State()
    choosing_date = State()
    choosing_time = State()
    confirm = State()


class ProfileForm(StatesGroup):
    input_full_name = State()
    input_birth_date = State()
    confirm = State()
