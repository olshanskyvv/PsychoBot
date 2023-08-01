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


class SessionMove(StatesGroup):
    choosing_date = State()
    choosing_time = State()
    confirm = State()


class ServiceEdit(StatesGroup):
    input_value = State()


class ServiceForm(StatesGroup):
    input_name = State()
    input_cost = State()
    input_duration = State()
    input_benefit = State()
