from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.driver import have_sessions


def get_agreement_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='С соглашением ознакомлен(а)',
        callback_data="agreement_confirm"
    )
    builder.adjust(1)
    return builder.as_markup()


async def get_record_choosing_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if not await have_sessions(telegram_id):
        builder.button(
            text='Первичная запись',
            callback_data='primary'
        )
    else:
        builder.button(
            text='Вторичная запись',
            callback_data='secondary'
        )
    builder.adjust(1)
    return builder.as_markup()


def get_profile_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Заполнить профиль',
                   callback_data='profile_fill')
    builder.adjust(1)
    return builder.as_markup()


def get_profile_confirm_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Все верно',
                   callback_data='profile_confirm')
    builder.button(text='Есть ошибка',
                   callback_data='profile_fill')
    builder.adjust(1)
    return builder.as_markup()


def get_profile_cancel_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Отмена',
                   callback_data='profile_cancel')
    builder.adjust(1)
    return builder.as_markup()

