from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from magic_filter import F

from db.driver import (
    get_users_nearest_session,
    delete_session_by_id,
    update_av_session_by_id
)
from handlers.recording.prosessing import process_data_callback, process_time_callback
from templates.session import (
    no_sessions,
    get_session_info_message,
    session_cancel
)
from templates.recording import (
    date_choice, get_confirmation_message,

)
from utils.keyboards.for_records import (
    get_available_dates_keyboard
)
from utils.keyboards.for_sessions import (
    get_session_info_keyboard,
    get_session_cancel_confirm_keyboard
)
from utils.callback_factories import (
    SessionAction,
    SessionActionFactory,
    DateCallbackFactory,
    TimeCallbackFactory
)
from utils.states import SessionMove

router = Router()


@router.message(Command('session'))
async def session_handler(message: Message) -> None:
    session = await get_users_nearest_session(message.from_user.id)
    if not session:
        await message.answer(text=no_sessions)
        return

    await message.answer(text=get_session_info_message(session),
                         reply_markup=get_session_info_keyboard(session))


@router.callback_query(SessionActionFactory.filter(F.action == SessionAction.CANCEL))
async def session_cancel_confirm_handler(callback: CallbackQuery,
                                         callback_data: SessionActionFactory) -> None:
    await callback.message.edit_text(text=session_cancel,
                                     reply_markup=get_session_cancel_confirm_keyboard(callback_data.id,
                                                                                      callback_data.duration))
    await callback.answer()


@router.callback_query(SessionActionFactory.filter(F.action == SessionAction.CANCEL_CONFIRM))
async def session_cancel_handler(callback: CallbackQuery,
                                 callback_data: SessionActionFactory) -> None:
    await delete_session_by_id(callback_data.id)

    await callback.message.edit_text(text=no_sessions,
                                     reply_markup=None)

    await callback.answer(text='Сессия отменена',
                          show_alert=True)


@router.callback_query(Text('move_cancel'))
@router.callback_query(Text('session_cancel_confirm_fail'))
async def new_session_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    session = await get_users_nearest_session(callback.from_user.id)
    if not session:
        await callback.message.edit_text(text=no_sessions,
                                         reply_markup=None)
        return

    await callback.message.edit_text(text=get_session_info_message(session),
                                     reply_markup=get_session_info_keyboard(session))
    await callback.answer()


@router.callback_query(SessionActionFactory.filter(F.action == SessionAction.MOVE))
async def session_move_date_handler(callback: CallbackQuery,
                                    callback_data: SessionActionFactory,
                                    state: FSMContext) -> None:
    await state.set_state(SessionMove.choosing_date)
    user_data = await state.get_data()
    user_data['session_id'] = callback_data.id
    user_data['duration'] = callback_data.duration
    await state.set_data(user_data)

    await callback.message.edit_text(text=date_choice,
                                     reply_markup=await get_available_dates_keyboard('move_cancel'))

    await callback.answer()


@router.callback_query(SessionMove.choosing_date,
                       DateCallbackFactory.filter())
async def session_move_date_handler(callback: CallbackQuery,
                                    callback_data: DateCallbackFactory,
                                    state: FSMContext) -> None:
    await process_data_callback(callback,
                                callback_data,
                                state,
                                SessionMove,
                                'move_cancel')


@router.callback_query(SessionMove.choosing_time,
                       TimeCallbackFactory.filter())
async def session_move_time_handler(callback: CallbackQuery,
                                    callback_data: TimeCallbackFactory,
                                    state: FSMContext) -> None:
    user_data = await state.get_data()
    await process_time_callback(callback,
                                callback_data,
                                state,
                                SessionMove,
                                get_confirmation_message,
                                user_data['duration'],
                                'move_cancel')


@router.callback_query(SessionMove.confirm,
                       Text('recording_confirm'))
async def session_move_confirm_handler(callback: CallbackQuery,
                                       state: FSMContext) -> None:
    user_data = await state.get_data()
    await update_av_session_by_id(user_data['session_id'],
                                  user_data['uuid'])
    session = await get_users_nearest_session(callback.from_user.id)
    await state.clear()

    await callback.message.edit_text(text=get_session_info_message(session),
                                     reply_markup=get_session_info_keyboard(session))

    await callback.answer(text='Сессия успешно перенесена',
                          show_alert=True)
