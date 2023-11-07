from datetime import datetime

from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db.driver import get_user_by_id, get_service_by_id, add_new_session
from db.models import UUID
from db.using import get_agreement_by_id
from handlers.recording.prosessing import process_data_callback, process_time_callback
from templates.recording import (
    profile_is_empty,
    service_choice,
    date_choice,
    get_confirmation_message,
    record_confirmed, no_agreement
)
from utils.keyboards.for_records import get_services_keyboard, get_available_dates_keyboard
from utils.callback_factories import ServiceCallbackFactory, DateCallbackFactory, TimeCallbackFactory
from utils.states import SecondaryRecord
from utils.scheduling.job_builders import confirm_checking_job, get_confirm_check_time, session_alert_job, \
    get_alert_time

router = Router()


@router.callback_query(Text('secondary'))
async def secondary_session_handler(callback: CallbackQuery, state: FSMContext) -> None:
    if not await get_agreement_by_id(callback.from_user.id):
        await callback.message.edit_text(text=no_agreement,
                                         reply_markup=None)
        await callback.answer()
        return
    user = await get_user_by_id(callback.from_user.id)
    if not (user.full_name and user.birth_date):
        await callback.message.edit_text(text=profile_is_empty,
                                         reply_markup=None)
        await callback.answer()
        return

    await state.set_state(SecondaryRecord.choosing_service)
    await callback.message.edit_text(text=service_choice,
                                     reply_markup=await get_services_keyboard(user.is_benefits))
    await callback.answer()


@router.callback_query(SecondaryRecord.choosing_service,
                       ServiceCallbackFactory.filter())
async def secondary_service_handler(callback: CallbackQuery,
                                    callback_data: ServiceCallbackFactory,
                                    state: FSMContext) -> None:
    user_data = await state.get_data()
    service = await get_service_by_id(callback_data.id)
    user_data['service_id'] = str(service.id)
    await state.set_data(user_data)

    await callback.message.edit_text(text=date_choice,
                                     reply_markup=await get_available_dates_keyboard('recording_cancel'))
    await state.set_state(SecondaryRecord.choosing_date)

    await callback.answer()


@router.callback_query(SecondaryRecord.choosing_date,
                       DateCallbackFactory.filter())
async def secondary_date_handler(callback: CallbackQuery,
                                 callback_data: DateCallbackFactory,
                                 state: FSMContext) -> None:
    await process_data_callback(callback,
                                callback_data,
                                state,
                                SecondaryRecord,
                                'recording_cancel')


@router.callback_query(SecondaryRecord.choosing_time,
                       TimeCallbackFactory.filter())
async def secondary_time_handler(callback: CallbackQuery,
                                 callback_data: TimeCallbackFactory,
                                 state: FSMContext) -> None:
    await process_time_callback(callback,
                                callback_data,
                                state,
                                SecondaryRecord,
                                get_confirmation_message,
                                50,
                                'recording_cancel')


@router.callback_query(SecondaryRecord.confirm,
                       Text('recording_confirm'))
async def secondary_confirm_handler(callback: CallbackQuery,
                                    state: FSMContext,
                                    scheduler: AsyncIOScheduler) -> None:
    user_data = await state.get_data()
    session_id = await add_new_session(callback.from_user.id,
                                       UUID(user_data['service_id']),
                                       UUID(user_data['uuid']))
    av_session_id = UUID(user_data['uuid'])
    checking_time = await get_confirm_check_time(av_session_id)
    alert_time = await get_alert_time(av_session_id)
    scheduler.add_job(confirm_checking_job, 'date',
                      args=[session_id], run_date=checking_time)
    scheduler.add_job(session_alert_job,
                      trigger='date',
                      args=[session_id],
                      run_date=alert_time)

    await state.clear()

    await callback.message.edit_text(text=record_confirmed,
                                     reply_markup=None)

    await callback.answer()
