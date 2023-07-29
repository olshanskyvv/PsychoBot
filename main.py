import asyncio
import logging

from aiogram import Dispatcher

import handlers
from db import driver
from utils import bot


logging.basicConfig(level=logging.INFO)


async def main() -> None:

    dp = Dispatcher()
    dp.include_router(handlers.router)

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
