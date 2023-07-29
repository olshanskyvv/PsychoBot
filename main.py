import asyncio
import logging

from aiogram import Bot, Dispatcher

import config
from handlers import agreement, recording
from db import driver


logging.basicConfig(level=logging.INFO)


async def main() -> None:

    dp = Dispatcher()
    dp.include_router(agreement.router)
    dp.include_router(recording.router)

    bot = Bot(config.TG_TOKEN, parse_mode="HTML")
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
