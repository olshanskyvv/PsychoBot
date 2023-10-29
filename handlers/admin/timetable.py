import datetime
import time

from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.callback_factories import (
    AvSessionDateFactory,
    NewAvTimeFactory,
    NewAvSessionFactory,
    DateCallbackFactory,
    AvSessionFactory,
    AvSessionDeleteFactory
)
from utils.keyboards.admin.for_timetable import (
    get_av_sessions_dates_keyboard,
    get_days_for_av_dates_keyboard,
    get_new_av_times_by_date_keyboard,
    get_av_sessions_count_keyboard,
    get_av_sessions_keyboard,
    get_av_session_actions_keyboard
)
from db.driver import add_new_av_sessions, get_available_sessions_by_id, delete_av_session_if_not_in_use
from utils.states import AdminAvView

router = Router()


@router.message(Command('timetable'))
async def timetable_command_handler(message: Message,
                                    state: FSMContext) -> None:
    await state.set_state(AdminAvView.choose_date)
    await message.answer(
        text="Доступные ячейки расписания",
        reply_markup=await get_av_sessions_dates_keyboard()
    )


@router.callback_query(Text('timetable_restart'))
async def timetable_restart_handler(callback: CallbackQuery,
                                    state: FSMContext) -> None:
    await state.set_state(AdminAvView.choose_date)
    await callback.message.edit_text(
        text="Доступные ячейки расписания",
        reply_markup=await get_av_sessions_dates_keyboard()
    )
    await callback.answer()


@router.callback_query(Text("av_session_add"))
async def add_av_session_handler(callback: CallbackQuery,
                                 state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(
        text="Выберите дату, когда хотите добавить ячейки",
        reply_markup=get_days_for_av_dates_keyboard()
    )
    await callback.answer()


@router.callback_query(AvSessionDateFactory.filter())
async def new_date_handler(callback: CallbackQuery,
                           callback_data: AvSessionDateFactory) -> None:
    selected_date = datetime.date.fromisoformat(callback_data.date)
    await callback.message.edit_text(
        text=f"Выберите время, с которого хотите добавлять ячейки {selected_date.strftime('%d.%m.%Y')}",
        reply_markup=await get_new_av_times_by_date_keyboard(selected_date)
    )
    await callback.answer()


@router.callback_query(NewAvTimeFactory.filter())
async def new_datetime_handler(callback: CallbackQuery,
                               callback_data: NewAvTimeFactory) -> None:
    selected_date = datetime.date.fromisoformat(callback_data.date)

    selected_datetime = datetime.datetime.fromisoformat(
        selected_date.isoformat() + " " + callback_data.time.replace(".", ":"))

    await callback.message.edit_text(
        text=f"Выберите, сколько ячеек хотите добавить {selected_datetime.strftime('%d.%m.%Y')}, " +
             f"начиная с {selected_datetime.strftime('%H:%M')}",
        reply_markup=get_av_sessions_count_keyboard(session_datetime=selected_datetime)
    )
    await callback.answer()


@router.callback_query(NewAvSessionFactory.filter())
async def new_sessions_handler(callback: CallbackQuery,
                               callback_data: NewAvSessionFactory,
                               state: FSMContext) -> None:
    await add_new_av_sessions(callback_data)

    await callback.answer(text="Ячейки записи добавлены успешно!",
                          show_alert=True)
    await timetable_restart_handler(callback, state)


@router.callback_query(AdminAvView.choose_date, DateCallbackFactory.filter())
async def date_choose_handler(callback: CallbackQuery,
                              callback_data: DateCallbackFactory,
                              state: FSMContext) -> None:
    await state.clear()
    date = datetime.date.fromisoformat(callback_data.date)
    await callback.message.edit_text(
        text=f"Доступные ячейки {date.strftime('%d.%m.%Y')}",
        reply_markup=await get_av_sessions_keyboard(date)
    )
    await callback.answer()


@router.callback_query(AvSessionFactory.filter())
async def av_session_handler(callback: CallbackQuery,
                             callback_data: AvSessionFactory) -> None:
    av_session = await get_available_sessions_by_id(callback_data.id)
    await callback.message.edit_text(
        text=f"Ячейка сессии {av_session.date.strftime('%d.%m.%Y')} в {av_session.time_begin.strftime('%H:%M')}",
        reply_markup=get_av_session_actions_keyboard(av_session.id)
    )
    await callback.answer()


@router.callback_query(AvSessionDeleteFactory.filter())
async def delete_session_handler(callback: CallbackQuery,
                                 callback_data: AvSessionDeleteFactory,
                                 state: FSMContext) -> None:
    is_deleted = await delete_av_session_if_not_in_use(callback_data.id)
    if not is_deleted:
        await callback.answer(
            text='Эта ячейка уже занята, её нельзя удалить',
            show_alert=True
        )
        return

    await callback.answer(
        text='Ячейка успешно удалена',
        show_alert=True
    )
    await timetable_restart_handler(callback, state)



