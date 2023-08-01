import uuid
from typing import Optional

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.driver import get_all_services
from db.models import UUID, Service
from utils.callback_factories import (
    ServiceCallbackFactory,
    ServiceActionFactory,
    ServiceAction,
    ServiceEditFactory,
    ServiceAttribute,
    BenefitEditFactory
)


async def get_services_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    services = await get_all_services()

    for service in services:
        builder.button(text=service.name,
                       callback_data=ServiceCallbackFactory(id=service.id))
    builder.button(text='Новая услуга',
                   callback_data='admin_service_new')

    builder.adjust(1)
    return builder.as_markup()


def get_service_action_keyboard(service_id: UUID) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Изменить",
                   callback_data=ServiceActionFactory(id=service_id,
                                                      action=ServiceAction.EDIT))
    builder.button(text="Удалить",
                   callback_data=ServiceActionFactory(id=service_id,
                                                      action=ServiceAction.DELETE_CONFIRM))
    builder.button(text="В начало",
                   callback_data="admin_service_restart")

    builder.adjust(1)
    return builder.as_markup()


def get_service_delete_confirm_keyboard(service_id: UUID) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Подтвердить',
                   callback_data=ServiceActionFactory(id=service_id,
                                                      action=ServiceAction.DELETE))
    builder.button(text='Отмена',
                   callback_data='admin_service_restart')

    builder.adjust(1)
    return builder.as_markup()


def get_service_edit_keyboard(service: Service) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=f'Наименование: {service.name}',
                   callback_data=ServiceEditFactory(id=service.id,
                                                    field=ServiceAttribute.NAME))
    builder.button(text=f'Цена: {service.cost} руб',
                   callback_data=ServiceEditFactory(id=service.id,
                                                    field=ServiceAttribute.COST))
    builder.button(text=f'Длительность: {service.duration} мин',
                   callback_data=ServiceEditFactory(id=service.id,
                                                    field=ServiceAttribute.DURATION))
    builder.button(text=f'Льготность: {"Да" if service.is_for_benefit else "Нет"}',
                   callback_data=ServiceEditFactory(id=service.id,
                                                    field=ServiceAttribute.BENEFIT))
    builder.button(text='Отмена',
                   callback_data='admin_service_restart')

    builder.adjust(1)
    return builder.as_markup()


def get_benefit_edit_keyboard(need_cancel: bool = True, service_id: UUID = None) -> InlineKeyboardMarkup:
    if not service_id:
        service_id = uuid.uuid4()

    builder = InlineKeyboardBuilder()

    builder.button(text='Льгота',
                   callback_data=BenefitEditFactory(id=service_id,
                                                    value=True))
    builder.button(text='Не льгота',
                   callback_data=BenefitEditFactory(id=service_id,
                                                    value=False))
    if need_cancel:
        builder.button(text='Отмена',
                       callback_data='admin_service_restart')
    builder.adjust(1)
    return builder.as_markup()
