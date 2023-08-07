from aiogram import Router, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from db.driver import (
    get_service_by_id,
    delete_service_by_id,
    update_service_filed, add_new_service
)
from db.models import Service
from templates.admin import (
    all_services,
    get_service_view_message,
    get_service_delete_confirm_message
)
from utils.keyboards.admin.for_services import (
    get_services_keyboard,
    get_service_action_keyboard,
    get_service_delete_confirm_keyboard,
    get_service_edit_keyboard,
    get_benefit_edit_keyboard,
    get_service_cancel_keyboard
)
from utils.callback_factories import (
    ServiceCallbackFactory,
    ServiceActionFactory,
    ServiceAction,
    ServiceEditFactory,
    ServiceAttribute,
    BenefitEditFactory
)
from utils.states import ServiceEdit, ServiceForm

router = Router()


@router.message(Command('services'))
async def services_command_handler(message: Message) -> None:
    await message.answer(text=all_services,
                         reply_markup=await get_services_keyboard())


@router.callback_query(Text('admin_service_restart'))
async def service_restart_handler(callback: CallbackQuery,
                                  state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(text=all_services,
                                     reply_markup=await get_services_keyboard())
    await callback.answer()


@router.callback_query(Text('admin_service_new'))
async def service_add_handler(callback: CallbackQuery,
                              state: FSMContext) -> None:
    user_data = await state.get_data()
    user_data['message_id'] = callback.message.message_id
    await state.set_data(user_data)
    await state.set_state(ServiceForm.input_name)

    await callback.message.edit_text(text='Введите наименование для услуги',
                                     reply_markup=get_service_cancel_keyboard())
    await callback.answer()


@router.message(ServiceForm.input_name)
async def service_name_input_handler(message: Message,
                                     state: FSMContext) -> None:
    user_data = await state.get_data()
    user_data['name'] = message.text
    await state.set_data(user_data)
    await state.set_state(ServiceForm.input_cost)
    bot = state.bot

    await bot.edit_message_text(text=f'{message.text}\n\nВведите стоимость в рублях',
                                chat_id=message.from_user.id,
                                message_id=user_data['message_id'],
                                reply_markup=get_service_cancel_keyboard())
    await message.delete()


@router.message(ServiceForm.input_cost)
async def service_cost_input_handler(message: Message,
                                     state: FSMContext) -> None:
    user_data = await state.get_data()
    user_data['cost'] = int(message.text)
    await state.set_data(user_data)
    await state.set_state(ServiceForm.input_duration)
    bot = state.bot

    await bot.edit_message_text(text=f'{user_data["name"]}\n'
                                     f'Стоимость: {message.text} руб\n\n'
                                     f'Введите длительность в минутах',
                                chat_id=message.from_user.id,
                                message_id=user_data['message_id'],
                                reply_markup=get_service_cancel_keyboard())
    await message.delete()


@router.message(ServiceForm.input_duration)
async def service_duration_input_handler(message: Message,
                                     state: FSMContext) -> None:
    user_data = await state.get_data()
    user_data['duration'] = int(message.text)
    await state.set_data(user_data)
    await state.set_state(ServiceForm.input_benefit)
    bot = state.bot

    await bot.edit_message_text(text=f'{user_data["name"]}\n'
                                     f'Стоимость: {user_data["cost"]} руб\n'
                                     f'Длительность: {message.text} мин\n\n'
                                     f'Выберите льготность',
                                reply_markup=get_benefit_edit_keyboard(need_cancel=True),
                                chat_id=message.from_user.id,
                                message_id=user_data['message_id'])
    await message.delete()


@router.callback_query(ServiceForm.input_benefit,
                       BenefitEditFactory.filter())
async def service_benefit_select(callback: CallbackQuery,
                                 callback_data: BenefitEditFactory,
                                 state: FSMContext) -> None:
    user_data = await state.get_data()
    await state.clear()

    service = Service(name=user_data['name'],
                      cost=user_data['cost'],
                      duration=user_data['duration'],
                      is_for_benefit=callback_data.value)
    service = await add_new_service(service)

    await callback.message.edit_text(text=get_service_view_message(service),
                                     reply_markup=get_service_action_keyboard(service.id))
    await callback.answer(text='Услуга добавлена успешно!',
                          show_alert=True)


@router.callback_query(ServiceCallbackFactory.filter())
async def service_view_handler(callback: CallbackQuery,
                               callback_data: ServiceCallbackFactory) -> None:
    service = await get_service_by_id(callback_data.id)

    await callback.message.edit_text(text=get_service_view_message(service),
                                     reply_markup=get_service_action_keyboard(service.id))
    await callback.answer()


@router.callback_query(ServiceActionFactory.filter(F.action == ServiceAction.DELETE_CONFIRM))
async def service_delete_confirm_handler(callback: CallbackQuery,
                                         callback_data: ServiceActionFactory) -> None:
    service = await get_service_by_id(callback_data.id)

    await callback.message.edit_text(text=get_service_delete_confirm_message(service),
                                     reply_markup=get_service_delete_confirm_keyboard(service.id))
    await callback.answer()


@router.callback_query(ServiceActionFactory.filter(F.action == ServiceAction.DELETE))
async def service_delete_handler(callback: CallbackQuery,
                                 callback_data: ServiceActionFactory) -> None:
    await delete_service_by_id(callback_data.id)
    await callback.answer(text="Услуга удалена успешно",
                          show_alert=True)
    await service_restart_handler(callback)


@router.callback_query(ServiceActionFactory.filter(F.action == ServiceAction.EDIT))
async def service_edit_handler(callback: CallbackQuery,
                               callback_data: ServiceActionFactory) -> None:
    service = await get_service_by_id(callback_data.id)

    await callback.message.edit_text(text="Какое поле хотите изменить?",
                                     reply_markup=get_service_edit_keyboard(service))
    await callback.answer()


@router.callback_query(ServiceEditFactory.filter(F.field == ServiceAttribute.BENEFIT))
async def service_edit_benefit_handler(callback: CallbackQuery,
                                       callback_data: ServiceEditFactory) -> None:
    await callback.message.edit_text(text='Какое значение хотите установить?',
                                     reply_markup=get_benefit_edit_keyboard(service_id=callback_data.id))
    await callback.answer()


@router.callback_query(BenefitEditFactory.filter())
async def service_edit_benefit_select_handler(callback: CallbackQuery,
                                         callback_data: BenefitEditFactory) -> None:
    await update_service_filed(callback_data.id, 'is_for_benefits', callback_data.value)
    service = await get_service_by_id(callback_data.id)

    await callback.message.edit_text(text='Какое поле хотите изменить?',
                                     reply_markup=get_service_edit_keyboard(service))
    await callback.answer(text='Льготность успешно установленна!',
                          show_alert=True)


@router.callback_query(ServiceEditFactory.filter())
async def service_edit_field_handler(callback: CallbackQuery,
                                     callback_data: ServiceEditFactory,
                                     state: FSMContext) -> None:
    user_data = await state.get_data()
    user_data['field'] = callback_data.field.value
    user_data['uuid'] = callback_data.id
    user_data['message_id'] = callback.message.message_id
    await state.set_data(user_data)
    await state.set_state(ServiceEdit.input_value)

    await callback.message.edit_text(text="Введите желаемое значение",
                                     reply_markup=get_service_cancel_keyboard())
    await callback.answer()


@router.message(ServiceEdit.input_value)
async def service_field_input_handler(message: Message,
                                      state: FSMContext) -> None:
    user_data = await state.get_data()
    bot = state.bot
    await state.clear()
    value = message.text
    try:
        value = int(value)
    except ValueError:
        pass

    await update_service_filed(user_data['uuid'],
                               user_data['field'],
                               value)
    service = await get_service_by_id(user_data['uuid'])

    await message.delete()
    await bot.edit_message_text(text=f'Услуга изменена успешна!\n\nКакое поле хотите изменить?',
                                chat_id=message.from_user.id,
                                message_id=user_data['message_id'],
                                reply_markup=get_service_edit_keyboard(service))
