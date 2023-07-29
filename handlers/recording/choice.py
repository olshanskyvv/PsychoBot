from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.keyboards.for_commands import get_record_choosing_keyboard
from templates.recording import general_choice

router = Router()


@router.message(Command('new_session'))
async def new_session_handler(message: Message) -> None:
    await message.answer(text=general_choice,
                         reply_markup=await get_record_choosing_keyboard(
                             telegram_id=message.from_user.id
                         ))


@router.callback_query(Text('recording_cancel'))
async def new_session_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(text=general_choice,
                                     reply_markup=await get_record_choosing_keyboard(
                                         telegram_id=callback.from_user.id
                                     ))
    await callback.answer()
