import datetime

from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.recording.prosessing import process_data_callback, process_time_callback
from utils.callback_factories import DateCallbackFactory, TimeCallbackFactory
from utils.states import PrimaryRecord
from templates.recording import (
    date_choice,
    get_time_choice_message,
    get_primary_confirmation_message,
    record_confirmed
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
    await process_data_callback(callback,
                                callback_data,
                                state,
                                PrimaryRecord)


@router.callback_query(PrimaryRecord.choosing_time,
                       TimeCallbackFactory.filter())
async def primary_time_handler(callback: CallbackQuery,
                               callback_data: TimeCallbackFactory,
                               state: FSMContext) -> None:
    await process_time_callback(callback,
                                callback_data,
                                state,
                                PrimaryRecord,
                                get_primary_confirmation_message)


@router.callback_query(PrimaryRecord.confirm,
                       Text('recording_confirm'))
async def primary_confirm_handler(callback: CallbackQuery,
                                  state: FSMContext) -> None:
    user_data = await state.get_data()
    await add_new_primary_session(callback.from_user.id, user_data['uuid'])
    await state.clear()

    await callback.message.edit_text(text=record_confirmed,
                                     reply_markup=None)

    await callback.answer()
