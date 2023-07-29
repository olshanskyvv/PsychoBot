import datetime

from aiogram.filters.callback_data import CallbackData

from db.models import UUID


class DateCallbackFactory(CallbackData, prefix='fabdate'):
    date: str


class TimeCallbackFactory(CallbackData, prefix='fabtime'):
    uuid: UUID
    time: str

