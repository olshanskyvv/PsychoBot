import datetime

from aiogram import Router, Bot
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from db.driver import get_user_by_id, set_name_and_birth_by_id
from templates.profile import (
    get_profile_data_message,
    profile_empty,
    get_birth_date_message,
    get_confirm_message
)
from utils import bot
from utils.keyboards.for_commands import get_profile_keyboard, get_profile_confirm_keyboard, get_profile_cancel_keyboard
from utils.states import ProfileForm

router = Router()


@router.message(Command('profile'))
async def profile_handler(message: Message) -> None:
    user = await get_user_by_id(message.from_user.id)
    if user.full_name and user.birth_date:
        await message.answer(text=get_profile_data_message(user.full_name, user.birth_date))
    else:
        await message.answer(text=profile_empty,
                             reply_markup=get_profile_keyboard())


@router.callback_query(Text('profile_cancel'))
async def profile_cancel_handler(callback: CallbackQuery,
                                 state: FSMContext) -> None:
    await state.clear()
    user = await get_user_by_id(callback.from_user.id)
    if user.full_name and user.birth_date:
        await callback.message.edit_text(text=get_profile_data_message(user.full_name, user.birth_date),
                                         reply_markup=None)
    else:
        await callback.message.edit_text(text=profile_empty,
                                         reply_markup=get_profile_keyboard())
    await callback.answer()


@router.callback_query(Text('profile_fill'))
async def profile_fill_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_data({})
    user_data = await state.get_data()
    user_data['message_id'] = callback.message.message_id
    await state.set_data(user_data)
    await state.set_state(ProfileForm.input_full_name)

    await callback.message.edit_text(text='Введите свои ФИО (полностью)',
                                     reply_markup=get_profile_cancel_keyboard())

    await callback.answer()


@router.message(ProfileForm.input_full_name)
async def profile_full_name_handler(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    user_data['full_name'] = message.text
    await state.set_data(user_data)
    await state.set_state(ProfileForm.input_birth_date)

    await bot.edit_message_text(text=get_birth_date_message(user_data['full_name']),
                                chat_id=message.from_user.id,
                                message_id=user_data['message_id'],
                                reply_markup=get_profile_cancel_keyboard())
    await message.delete()


@router.message(ProfileForm.input_birth_date)
async def profile_birth_date_handler(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()

    try:
        birth_date = datetime.datetime.strptime(message.text, '%d.%m.%Y').date()
    except ValueError:
        await bot.edit_message_text(text=get_birth_date_message(user_data['full_name'], True),
                                    chat_id=message.chat.id,
                                    message_id=user_data['message_id'],
                                    reply_markup=get_profile_cancel_keyboard())
        await message.delete()
        return

    user_data['birth_date'] = birth_date
    await state.set_data(user_data)
    await state.set_state(ProfileForm.confirm)

    await bot.edit_message_text(text=get_confirm_message(user_data['full_name'],
                                                         birth_date),
                                chat_id=message.chat.id,
                                message_id=user_data['message_id'],
                                reply_markup=get_profile_confirm_keyboard())
    await message.delete()


@router.callback_query(Text('profile_confirm'))
async def profile_confirm_handler(callback: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    await set_name_and_birth_by_id(telegram_id=callback.from_user.id,
                                   full_name=user_data['full_name'],
                                   birth_date=user_data['birth_date'])
    await state.clear()

    await callback.message.edit_text(text=get_profile_data_message(full_name=user_data['full_name'],
                                                                   birth_date=user_data['birth_date']),
                                     reply_markup=None)
