import asyncio
import logging

from aiogram import Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat

import handlers
from db import driver
from utils import bot
from config import ADMIN_ID, OWNER_ID

logging.basicConfig(level=logging.INFO)


async def set_commands() -> None:
    # Set default commands
    default_commands = [
            BotCommand(command='start',
                       description='Запуск бота и доступные команды'),
            BotCommand(command='agreement',
                       description='Пользовательское соглашение'),
            BotCommand(command='profile',
                       description='Просмотр и заполнение персональных данных'),
            BotCommand(command='session',
                       description='Просмотр, подтверждение, перенос и отмена текущей сессии'),
            BotCommand(command='new_session',
                       description='Планирование новой сессии'),
        ]
    await bot.set_my_commands(
        default_commands,
        BotCommandScopeDefault()
    )
    # Set admin commands
    admin_commands = [
        BotCommand(command='sessions',
                   description='Просмотр ближайших сессий'),
        BotCommand(command='services',
                   description='Просмотр и изменение услуг'),
        BotCommand(command='timetable',
                   description='Просмотр и изменение сетки расписания'),
    ]
    await bot.set_my_commands(
        [*default_commands, *admin_commands],
        # [*default_commands],
        BotCommandScopeChat(chat_id=ADMIN_ID)
    )
    await bot.set_my_commands(
        [*default_commands, *admin_commands],
        # [*default_commands],
        BotCommandScopeChat(chat_id=OWNER_ID)
    )


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(handlers.router)

    await set_commands()
    await driver.get_connection()

    await dp.start_polling(bot)


def run() -> None:
    try:
        asyncio.run(main())
    except RuntimeError:
        import traceback

        logging.warning(traceback.format_exc())
    finally:
        driver.close_connection()


if __name__ == "__main__":
    run()
