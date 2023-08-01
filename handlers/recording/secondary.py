from datetime import datetime

from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from db.driver import get_user_by_id, get_service_by_id, add_new_session
from handlers.recording.prosessing import process_data_callback, process_time_callback
from templates.recording import (
    profile_is_empty,
    service_choice,
    date_choice,
    get_confirmation_message,
    record_confirmed
)
from utils.keyboards.for_records import get_services_keyboard, get_available_dates_keyboard
from utils.callback_factories import ServiceCallbackFactory, DateCallbackFactory, TimeCallbackFactory
from utils.states import SecondaryRecord

router = Router()


@router.callback_query(Text('secondary'))
async def secondary_session_handler(callback: CallbackQuery, state: FSMContext) -> None:
    user = await get_user_by_id(callback.from_user.id)
    if not (user.full_name and user.birth_date):
        await callback.message.edit_text(text=profile_is_empty,
                                         reply_markup=None)
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
    user_data['service'] = service
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
                                    state: FSMContext) -> None:
    user_data = await state.get_data()
    await add_new_session(callback.from_user.id,
                          user_data['service'].id,
                          user_data['uuid'])
    await state.clear()

    await callback.message.edit_text(text=record_confirmed,
                                     reply_markup=None)

    await callback.answer()
