import datetime

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.driver import get_available_dates, get_available_times_by_date


async def get_available_dates_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    av_dates = await get_available_dates()
    for av_date in av_dates:
        date_string = datetime.date.fromisoformat(av_date.date).strftime('%d.%m.%Y')
        builder.button(text=date_string,
                       callback_data=av_date)
    builder.button(text=f"Вернуться в начало{' (нет доступных записей)' if not av_dates else ''}",
                   callback_data='recording_cancel')
    builder.adjust(1)
    return builder.as_markup()


async def get_available_times_keyboard(date: datetime.date) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    av_times = await get_available_times_by_date(date)
    for av_time in av_times:
        time_string = datetime.datetime.strptime(av_time.time, '%H.%M').strftime('%H:%M')
        builder.button(text=time_string,
                       callback_data=av_time)
    builder.button(text=f"Вернуться в начало{' (нет доступных записей)' if not av_times else ''}",
                   callback_data='recording_cancel')
    builder.adjust(1)
    return builder.as_markup()


async def get_record_confirmation_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Подтвердить',
                   callback_data='recording_confirm')
    builder.button(text='Вернуться в начало',
                   callback_data='recording_cancel')
    builder.adjust(1)
    return builder.as_markup()