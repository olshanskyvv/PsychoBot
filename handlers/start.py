import logging
from random import randint

from aiogram import Router, types
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder

from templates.messages import agreement, agreement_confirmed
from utils.keyboards import get_agreement_keyboard

router = Router()


@router.message(Command(commands=['start']))
async def start_handler(message: Message) -> None:
    # TODO: проверка на соглашение
    await message.answer(text=agreement,
                         reply_markup=get_agreement_keyboard())


@router.callback_query(Text('agreement_confirm'))
async def confirm_agreement_handler(callback: CallbackQuery) -> None:
    # TODO: проверка на соглашение и пометка в бд
    await callback.message.answer(
        text=agreement_confirmed
    )
    await callback.message.delete_reply_markup()
    await callback.answer()

