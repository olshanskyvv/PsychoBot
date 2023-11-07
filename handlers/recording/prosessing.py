import datetime
from typing import Callable, Type

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from db.models import Minutes
from templates.recording import get_time_choice_message
from utils.callback_factories import DateCallbackFactory, TimeCallbackFactory
from utils.keyboards.for_records import get_available_times_keyboard, get_record_confirmation_keyboard
from utils.states import PrimaryRecord, SecondaryRecord, SessionMove


async def process_data_callback(callback: CallbackQuery,
                                callback_data: DateCallbackFactory,
                                state: FSMContext,
                                states_group: Type[PrimaryRecord | SecondaryRecord | SessionMove],
                                cancel_text: str) -> None:
    user_data = await state.get_data()
    date = datetime.date.fromisoformat(callback_data.date)
    user_data['date'] = date.isoformat()
    await state.set_data(user_data)

    await callback.message.edit_text(text=get_time_choice_message(date),
                                     reply_markup=await get_available_times_keyboard(date, cancel_text))
    await state.set_state(states_group.choosing_time)

    await callback.answer()


async def process_time_callback(callback: CallbackQuery,
                                callback_data: TimeCallbackFactory,
                                state: FSMContext,
                                states_group: Type[PrimaryRecord | SecondaryRecord | SessionMove],
                                message_text_getter: Callable[[datetime.date, datetime.time, Minutes], str],
                                duration: Minutes,
                                cancel_text: str) -> None:
    user_data = await state.get_data()
    time = datetime.datetime.strptime(callback_data.time, '%H.%M').time()
    user_data['time'] = time.isoformat()
    user_data['uuid'] = str(callback_data.uuid)
    await state.set_data(user_data)

    await callback.message.edit_text(
        text=message_text_getter(datetime.date.fromisoformat(user_data['date']), time, duration),
        reply_markup=await get_record_confirmation_keyboard(cancel_text))
    await state.set_state(states_group.confirm)

    await callback.answer()
