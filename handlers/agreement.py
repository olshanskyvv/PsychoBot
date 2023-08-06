from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery

import templates.agreements as agreements
from utils.keyboards.for_commands import get_agreement_keyboard
from db.using import get_agreement_by_id
from db.driver import set_agreement_true

router = Router()


@router.message(Command('agreement'))
async def agreement_command_handler(message: Message) -> None:
    keyboard = None
    result = await get_agreement_by_id(message.from_user.id)
    if not result:
        keyboard = get_agreement_keyboard()
    await message.answer(text=agreements.agreement,
                         reply_markup=keyboard)


@router.callback_query(Text('agreement_confirm'))
async def confirm_agreement_handler(callback: CallbackQuery) -> None:
    if await get_agreement_by_id(callback.from_user.id):
        await callback.answer(
            text=agreements.agreement_already_confirmed,
            show_alert=True
        )
    else:
        await callback.message.answer(
            text=agreements.agreement_confirm)
        await set_agreement_true(callback.from_user.id)
    await callback.message.delete_reply_markup()
    await callback.answer()
