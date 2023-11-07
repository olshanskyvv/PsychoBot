import asyncio
import logging

from aiogram import Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from aiogram.fsm.storage.redis import RedisStorage, Redis
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import handlers
from db import driver
from utils import bot
from config import ADMIN_ID, OWNER_ID, REDIS_HOST, REDIS_PORT
from utils.scheduling.schedule_middlewares import ScheduleCallbackMiddleware


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
        BotCommandScopeChat(chat_id=ADMIN_ID)
    )
    await bot.set_my_commands(
        [*default_commands, *owner_commands],
        BotCommandScopeChat(chat_id=OWNER_ID)
    )


async def main() -> None:
    storage = RedisStorage(redis=Redis(
        host=REDIS_HOST,
        port=REDIS_PORT
    ))

    job_stores = {
        'default': RedisJobStore(host='localhost', port=6379)
    }

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow", jobstores=job_stores)
    scheduler.start()
    # scheduler.remove_all_jobs()

    dp = Dispatcher(storage=storage)
    dp.callback_query.middleware.register(ScheduleCallbackMiddleware(scheduler))
    dp.include_router(handlers.router)

    await set_commands()
    await driver.get_connection()
    try:
        await dp.start_polling(bot)
    except RuntimeError:
        import traceback

        logging.warning(traceback.format_exc())
    finally:
        await driver.async_close_connection()
        scheduler.shutdown()
        logging.info('Clear')


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run()
