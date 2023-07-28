import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message

import config
import handlers.start


logging.basicConfig(level=logging.INFO)


async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(handlers.start.router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(config.TG_TOKEN, parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot)


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run()
