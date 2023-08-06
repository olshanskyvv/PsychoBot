import datetime

from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery

from db.driver import get_full_session_by_id
from templates.admin import get_session_view_message
from utils.keyboards.admin.for_sessions import (
    get_session_dates_keyboard,
    get_sessions_by_date_keyboard,
    get_session_restart_keyboard
)
from utils.callback_factories import SessionDateFactory, SessionFactory

router = Router()


@router.message(Command("sessions"))
async def sessions_command_handler(message: Message) -> None:
    await message.answer(text='Дни ближайшей недели, когда у Вас есть запланированные сессии:',
                         reply_markup=await get_session_dates_keyboard())


@router.callback_query(Text('session_view_cancel'))
async def sessions_restart_handler(callback: CallbackQuery) -> None:
    await callback.message.edit_text(text='Дни ближайшей недели, когда у Вас есть запланированные сессии:',
                                     reply_markup=await get_session_dates_keyboard())
    await callback.answer()


@router.callback_query(SessionDateFactory.filter())
async def session_date_handler(callback: CallbackQuery,
                               callback_data: SessionDateFactory) -> None:
    date = datetime.date.fromisoformat(callback_data.date)
    await callback.message.edit_text(text=f'Запланированные сессии {date.strftime("%d.%m.%Y")}',
                                     reply_markup=await get_sessions_by_date_keyboard(date))
    await callback.answer()


@router.callback_query(SessionFactory.filter())
async def session_view_handler(callback: CallbackQuery,
                               callback_data: SessionFactory) -> None:
    session = await get_full_session_by_id(callback_data.id)

    await callback.message.edit_text(text=get_session_view_message(session),
                                     reply_markup=get_session_restart_keyboard())

    await callback.answer()

