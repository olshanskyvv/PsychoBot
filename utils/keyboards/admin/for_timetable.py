import uuid
import datetime

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.driver import get_available_dates, get_available_times_by_date, get_av_sessions_by_date
from db.models import UUID, Service
from utils.callback_factories import (
    AvSessionDateFactory,
    NewAvTimeFactory,
    NewAvSessionFactory,
    AvSessionFactory,
    AvSessionDeleteFactory
)


async def get_av_sessions_dates_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    av_dates = await get_available_dates()
    for av_date in av_dates:
        date_string = datetime.date.fromisoformat(av_date.date).strftime('%d.%m.%Y')
        builder.button(
            text=date_string,
            callback_data=av_date
        )

    builder.button(
        text="Добавить новые ячейки",
        callback_data="av_session_add"
    )

    builder.adjust(1)
    return builder.as_markup()


weekdays = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье",
}


def get_days_for_av_dates_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    dates = [datetime.date.today() + datetime.timedelta(days=i) for i in range(1, 15)]
    for date in dates:
        builder.button(
            text=f"{date.strftime('%d.%m.%Y')} {weekdays[date.weekday()]}",
            callback_data=AvSessionDateFactory(date=date.isoformat())
        )
    builder.button(
        text="В начало",
        callback_data='timetable_restart'
    )
    builder.adjust(1)
    return builder.as_markup()


async def get_new_av_times_by_date_keyboard(date: datetime.date) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    min_time = None
    if date == datetime.date.today() + datetime.timedelta(days=1):
        min_time = datetime.datetime.now().time()

    av_times = await get_available_times_by_date(date, min_time)
    av_times = set(map(lambda time_fab: datetime.datetime.strptime(time_fab.time, '%H.%M').time(), av_times))

    cur_time = datetime.datetime(year=1, month=1, day=1, hour=9)
    if min_time:
        cur_time = datetime.datetime(year=1, month=1, day=1, hour=max(9, min_time.hour + 1))
    while cur_time <= datetime.datetime(year=1, month=1, day=1, hour=21):
        if not cur_time.time() in av_times:
            builder.button(
                text=cur_time.strftime("%H:%M"),
                callback_data=NewAvTimeFactory(date=date.isoformat(),
                                               time=cur_time.time().strftime('%H.%M'))
            )
        cur_time = cur_time + datetime.timedelta(hours=1)

    builder.button(
        text="В начало",
        callback_data='timetable_restart'
    )
    builder.adjust(1)
    return builder.as_markup()


def get_av_sessions_count_keyboard(session_datetime: datetime.datetime) -> InlineKeyboardMarkup:
    time = session_datetime.time()

    builder = InlineKeyboardBuilder()
    builder.button(
        text="1 сессия",
        callback_data=NewAvSessionFactory(
            datetime=session_datetime.isoformat().replace(':', '+'),
            count=1
        )
    )
    if time.hour <= 20:
        builder.button(
            text="2 сессии",
            callback_data=NewAvSessionFactory(
                datetime=session_datetime.isoformat().replace(':', '+'),
                count=2
            )
        )
    if time.hour <= 19:
        builder.button(
            text="3 сессии",
            callback_data=NewAvSessionFactory(
                datetime=session_datetime.isoformat().replace(':', '+'),
                count=3
            )
        )

    builder.button(
        text="В начало",
        callback_data='timetable_restart'
    )
    builder.adjust(1)
    return builder.as_markup()


async def get_av_sessions_keyboard(date: datetime.date) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    av_sessions = await get_av_sessions_by_date(date)
    for av_session in av_sessions:
        builder.button(
            text=av_session.time.replace('.', ':'),
            callback_data=av_session
        )

    builder.button(
        text="В начало",
        callback_data='timetable_restart'
    )
    builder.adjust(1)
    return builder.as_markup()


def get_av_session_actions_keyboard(session_id: UUID) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Удалить",
        callback_data=AvSessionDeleteFactory(id=session_id)
    )

    builder.button(
        text="В начало",
        callback_data='timetable_restart'
    )
    builder.adjust(1)
    return builder.as_markup()

