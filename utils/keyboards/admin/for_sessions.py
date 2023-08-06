import datetime

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.driver import get_session_days, get_sessions_by_date_and_time
from utils.callback_factories import SessionDateFactory, SessionFactory


async def get_session_dates_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    dates = await get_session_days()
    for date in dates:
        builder.button(text=date.strftime('%d.%m.%Y'),
                       callback_data=SessionDateFactory(date=date.isoformat()))
    builder.adjust(1)
    return builder.as_markup()


async def get_sessions_by_date_keyboard(date: datetime.date) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    time = None
    if date == datetime.date.today():
        time = datetime.datetime.now().time()
    sessions = await get_sessions_by_date_and_time(date, time)
    for session in sessions:
        builder.button(text=f'{session.time.strftime("%H:%M")} - {session.name}',
                       callback_data=SessionFactory(id=session.id))

    builder.button(text='В начало',
                   callback_data='session_view_cancel')
    builder.adjust(1)
    return builder.as_markup()


def get_session_restart_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='В начало',
                   callback_data='session_view_cancel')
    builder.adjust(1)
    return builder.as_markup()


