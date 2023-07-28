import asyncio
import logging

import asyncpg
from typing import Optional

from config import PG_USER, PG_HOST, PG_DATABASE_NAME


async def get_connection() -> asyncpg.Connection:
    if not getattr(get_connection, 'connection', None):
        get_connection.connection = \
            await asyncpg.connect(f'postgresql://{PG_USER}@{PG_HOST}/{PG_DATABASE_NAME}')
        logging.info('DB connected')

    return get_connection.connection


async def _async_close_connection() -> None:
    await (await get_connection()).close()
    logging.info('DB closed')


def close_connection() -> None:
    asyncio.run(_async_close_connection())




