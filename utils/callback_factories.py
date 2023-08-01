import datetime
from enum import Enum
from typing import Literal

from aiogram.filters.callback_data import CallbackData

from db.models import UUID, Service, Minutes


class DateCallbackFactory(CallbackData, prefix='fabdate'):
    date: str


class TimeCallbackFactory(CallbackData, prefix='fabtime'):
    uuid: UUID
    time: str


class ServiceCallbackFactory(CallbackData, prefix='fabservice'):
    id: UUID


class SessionAction(Enum):
    CANCEL = 'cancel'
    CANCEL_CONFIRM = 'confirm'
    MOVE = 'move'
    PAY = 'pay'


class SessionActionFactory(CallbackData, prefix='fabsession'):
    id: UUID
    duration: Minutes
    action: SessionAction

