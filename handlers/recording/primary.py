import datetime

from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db.models import UUID
from handlers.recording.prosessing import process_data_callback, process_time_callback
from utils.callback_factories import DateCallbackFactory, TimeCallbackFactory
from utils.states import PrimaryRecord
from templates.recording import (
    date_choice,
    get_confirmation_message,
    record_confirmed
)
from utils.keyboards.for_records import (
    get_available_dates_keyboard
)
from db.using import add_new_primary_session
from utils.scheduling.job_builders import confirm_checking_job, get_confirm_check_time

router = Router()


@router.callback_query(Text('primary'))
async def primary_session_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(text=date_choice,
                                     reply_markup=await get_available_dates_keyboard('recording_cancel'))
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
                                PrimaryRecord,
                                'recording_cancel')


@router.callback_query(PrimaryRecord.choosing_time,
                       TimeCallbackFactory.filter())
async def primary_time_handler(callback: CallbackQuery,
                               callback_data: TimeCallbackFactory,
                               state: FSMContext) -> None:
    await process_time_callback(callback,
                                callback_data,
                                state,
                                PrimaryRecord,
                                get_confirmation_message,
                                30,
                                'recording_cancel')


@router.callback_query(PrimaryRecord.confirm,
                       Text('recording_confirm'))
async def primary_confirm_handler(callback: CallbackQuery,
                                  state: FSMContext,
                                  scheduler: AsyncIOScheduler) -> None:
    user_data = await state.get_data()
    session_id = await add_new_primary_session(callback.from_user.id, user_data['uuid'])

    checking_time = await get_confirm_check_time(UUID(user_data['uuid']))
    scheduler.add_job(confirm_checking_job, 'date',
                      args=[session_id], run_date=checking_time)
    await state.clear()

    await callback.message.edit_text(text=record_confirmed,
                                     reply_markup=None)

    await callback.answer()
