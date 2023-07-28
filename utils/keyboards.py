from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_agreement_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text='С соглашением ознакомлен(а)',
        callback_data="agreement_confirm"
    ))
    buttons = [[InlineKeyboardButton(
        text='С соглашением ознакомлен(а)',
        callback_data="agreement_confirm"
    )
    ]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
    # return builder.as_markup()


