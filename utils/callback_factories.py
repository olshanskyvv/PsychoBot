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


class ServiceAction(Enum):
    EDIT = 'edit'
    DELETE_CONFIRM = 'delete_confirm'
    DELETE = 'delete'


class ServiceActionFactory(CallbackData, prefix='fabactserv'):
    id: UUID
    action: ServiceAction


class SessionAction(Enum):
    CANCEL = 'cancel'
    CANCEL_CONFIRM = 'confirm'
    MOVE = 'move'
    PAY = 'pay'


class SessionActionFactory(CallbackData, prefix='fabsession'):
    id: UUID
    duration: Minutes
    action: SessionAction


class ServiceAttribute(Enum):
    NAME = 'name'
    COST = 'cost'
    DURATION = 'duration'
    BENEFIT = 'is_for_benefits'


class ServiceEditFactory(CallbackData, prefix='fabservedit'):
    id: UUID
    field: ServiceAttribute


class BenefitEditFactory(CallbackData, prefix='fabbenefit'):
    id: UUID
    value: bool

