from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from db.driver import get_user_by_id, add_new_user
from db.models import BotUser
from templates.agreements import start

router = Router()


@router.message(Command('start'))
async def start_command_handler(message: Message) -> None:
    bot_user = await get_user_by_id(message.from_user.id)
    if not bot_user:
        user = BotUser(telegram_id=message.from_user.id,
                       username=message.from_user.username)
        await add_new_user(user)

    await message.answer(start)

