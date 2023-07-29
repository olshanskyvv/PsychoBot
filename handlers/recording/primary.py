from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from utils.callback_factories import DateCallbackFactory, TimeCallbackFactory
from utils.states import PrimaryRecord
from templates.recording import (
    date_choice,
    get_time_choice_message,
    get_primary_confirmation_message,
    primary_record_confirmed
)
from utils.keyboards.for_records import (
    get_available_dates_keyboard,
    get_available_times_keyboard,
    get_record_confirmation_keyboard
)
from db.using import add_new_primary_session

router = Router()


@router.callback_query(Text('primary'))
async def primary_session_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(text=date_choice,
                                     reply_markup=await get_available_dates_keyboard())
    await state.set_state(PrimaryRecord.choosing_date)

    await callback.answer()


@router.callback_query(PrimaryRecord.choosing_date,
                       DateCallbackFactory.filter())
async def primary_date_handler(callback: CallbackQuery,
                               callback_data: DateCallbackFactory,
                               state: FSMContext) -> None:
    user_data = await state.get_data()
    user_data['date'] = callback_data.date
    await state.set_data(user_data)

    await callback.message.edit_text(text=get_time_choice_message(callback_data.date),
                                     reply_markup=await get_available_times_keyboard(callback_data.date))
    await state.set_state(PrimaryRecord.choosing_time)

    await callback.answer()


@router.callback_query(PrimaryRecord.choosing_time,
                       TimeCallbackFactory.filter())
async def primary_time_handler(callback: CallbackQuery,
                               callback_data: TimeCallbackFactory,
                               state: FSMContext) -> None:
    user_data = await state.get_data()
    user_data['time'] = callback_data.time
    user_data['uuid'] = callback_data.uuid
    await state.set_data(user_data)

    await callback.message.edit_text(
        text=get_primary_confirmation_message(user_data['date'], user_data['time']),
        reply_markup=await get_record_confirmation_keyboard())
    await state.set_state(PrimaryRecord.confirm)

    await callback.answer()


@router.callback_query(PrimaryRecord.confirm,
                       Text('recording_confirm'))
async def primary_confirm_handler(callback: CallbackQuery,
                                  state: FSMContext) -> None:
    user_date = await state.get_data()
    await add_new_primary_session(callback.from_user.id, user_date['uuid'])

    await callback.message.delete_reply_markup()
    await callback.message.edit_text(text=primary_record_confirmed)

    await callback.answer()
