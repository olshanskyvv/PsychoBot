from enum import Enum

from aiogram.filters.callback_data import CallbackData

from db.models import UUID, Minutes


class DateCallbackFactory(CallbackData, prefix='FabDate'):
    date: str


class TimeCallbackFactory(CallbackData, prefix='FabTime'):
    uuid: UUID
    time: str


class ServiceCallbackFactory(CallbackData, prefix='FabService'):
    id: UUID


class ServiceAction(Enum):
    EDIT = 'edit'
    DELETE_CONFIRM = 'delete_confirm'
    DELETE = 'delete'


class ServiceActionFactory(CallbackData, prefix='FabActServ'):
    id: UUID
    action: ServiceAction


class SessionAction(Enum):
    CANCEL = 'cancel'
    CANCEL_CONFIRM = 'confirm'
    MOVE = 'move'
    PAY = 'pay'


class SessionActionFactory(CallbackData, prefix='FabSession'):
    id: UUID
    duration: Minutes
    action: SessionAction


class ServiceAttribute(Enum):
    NAME = 'name'
    COST = 'cost'
    DURATION = 'duration'
    BENEFIT = 'is_for_benefits'


class ServiceEditFactory(CallbackData, prefix='FabServEdit'):
    id: UUID
    field: ServiceAttribute


class BenefitEditFactory(CallbackData, prefix='FabBenefit'):
    id: UUID
    value: bool


class SessionDateFactory(CallbackData, prefix='FabSessionDate'):
    date: str


class SessionFactory(CallbackData, prefix='FabSesView'):
    id: UUID


