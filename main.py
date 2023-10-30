import asyncio
import logging

from aiogram import Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from aiogram.fsm.storage.redis import RedisStorage, Redis

import handlers
from db import driver
from utils import bot
from config import ADMIN_ID, OWNER_ID, REDIS_HOST, REDIS_PORT

logging.basicConfig(level=logging.INFO)


async def set_commands() -> None:
    # Set default commands
    default_commands = [
            BotCommand(command='start',
                       description='Запуск бота и доступные команды'),
            BotCommand(command='agreement',
                       description='Пользовательское соглашение'),
        ]
    client_commands = [
            BotCommand(command='profile',
                       description='Просмотр и заполнение персональных данных'),
            BotCommand(command='session',
                       description='Просмотр, подтверждение, перенос и отмена текущей сессии'),
            BotCommand(command='new_session',
                       description='Планирование новой сессии'),
    ]
    await bot.set_my_commands(
        [*default_commands, *client_commands],
        BotCommandScopeDefault()
    )
    # Set admin commands
    owner_commands = [
        BotCommand(command='sessions',
                   description='Просмотр ближайших сессий'),
        BotCommand(command='services',
                   description='Просмотр и изменение услуг'),
        BotCommand(command='timetable',
                   description='Просмотр и изменение сетки расписания'),
    ]
    await bot.set_my_commands(
        [*default_commands, *client_commands, *owner_commands],
        # [*default_commands],
        BotCommandScopeChat(chat_id=ADMIN_ID)
    )
    await bot.set_my_commands(
        [*default_commands, *owner_commands],
        # [*default_commands],
        BotCommandScopeChat(chat_id=OWNER_ID)
    )


async def main() -> None:
    storage = RedisStorage(redis=Redis(
        host=REDIS_HOST,
        port=REDIS_PORT
    ))

    # dp = Dispatcher()
    dp = Dispatcher(storage=storage)
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
