import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message

import config
from handlers import agreement
from db import driver


logging.basicConfig(level=logging.INFO)


async def main() -> None:

    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(agreement.router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(config.TG_TOKEN, parse_mode="HTML")
    await driver.get_connection()
    # And the run events dispatching
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
