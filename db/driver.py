import asyncio
import datetime
import logging

import asyncpg
from typing import Iterable, Optional

from config import PG_USER, PG_HOST, PG_DATABASE_NAME
import db.queries as queries
from db.models import BotUser, Service, AvailableSession, Session, UUID


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


async def init_db_if_empty() -> None:
    conn = await get_connection()
    await conn.execute(queries.init_query)


async def add_new_user(bot_user: BotUser) -> BotUser:
    conn = await get_connection()
    await conn.execute('''
        insert into bot_users (telegram_id) values ($1)
    ''', bot_user.telegram_id)
    return bot_user


async def add_new_service(service: Service) -> Service:
    conn = await get_connection()
    row = await conn.fetchrow("""
        insert into services (id, name, cost, duration, is_for_benefits)
        values (gen_random_uuid(), $1, $2, $3, $4)
        returning id
    """, service.name, service.cost, service.duration, service.is_for_benefit)
    service.id = row.get('id', None)
    return service


async def add_new_available_session(av_session: AvailableSession) -> AvailableSession:
    conn = await get_connection()
    row = await conn.fetchrow("""
    insert into available_sessions (id, date, time_begin)
    values (gen_random_uuid(), $1, $2)
    returning id
    """, av_session.date, av_session.time_begin)
    av_session.id = row.get('id', None)
    return av_session


async def add_new_session(session: Session) -> Session:
    conn = await get_connection()
    row = await conn.fetchrow("""
    insert into sessions (id, bot_user_id, service_id, available_session_id) 
    values (gen_random_uuid(), $1, $2, $3)
    returning id
    """, session.user.telegram_id, session.service.id, session.available_session.id)
    session.id = row['id']
    return session


async def get_user_by_id(telegram_id: int) -> Optional[BotUser]:
    conn = await get_connection()
    row = await conn.fetchrow("""
    select * from bot_users where telegram_id = $1
    """, telegram_id)
    return BotUser(**row) if row else None


async def get_service_by_id(service_id: UUID) -> Service:
    conn = await get_connection()
    row = await conn.fetchrow("""
    select * from services where id = $1
    """, service_id)
    return Service(**row)


async def get_available_sessions_by_id(av_session_id: UUID) -> AvailableSession:
    conn = await get_connection()
    row = await conn.fetchrow("""
    select * from available_sessions where id = $1
    """, av_session_id)
    return AvailableSession(**row)


async def get_session_by_id(session_id: UUID) -> Session:
    conn = await get_connection()
    row = await conn.fetchrow("""
    select * from sessions where id = $1
    """, session_id)
    bot_user = await get_user_by_id(row['bot_user_id'])
    service = await get_service_by_id(row['service_id'])
    av_session = await get_available_sessions_by_id(row['available_session_id'])
    return Session(id=row.get('id', None),
                   user=bot_user,
                   service=service,
                   available_session=av_session,
                   is_confirmed=row.get('is_confirmed', None))


async def set_agreement_true(telegram_id) -> None:
    conn = await get_connection()
    await conn.execute('''
    update bot_users 
    set agreement = true 
    where telegram_id = $1
    ''', telegram_id)
