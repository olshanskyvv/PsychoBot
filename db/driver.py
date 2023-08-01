import asyncio
import datetime
import logging

import asyncpg
from typing import Iterable, Optional

from config import PG_USER, PG_HOST, PG_DATABASE_NAME
import db.queries as queries
from db.models import BotUser, Service, AvailableSession, Session, UUID, SessionView
from utils.callback_factories import TimeCallbackFactory, DateCallbackFactory, ServiceCallbackFactory


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
        insert into services (name, cost, duration, is_for_benefits)
        values ($1, $2, $3, $4)
        returning id
    """, service.name, service.cost, service.duration, service.is_for_benefit)
    service.id = row.get('id', None)
    return service


async def add_new_available_session(av_session: AvailableSession) -> AvailableSession:
    conn = await get_connection()
    row = await conn.fetchrow("""
    insert into available_sessions (date, time_begin)
    values ($1, $2)
    returning id
    """, av_session.date, av_session.time_begin)
    av_session.id = row.get('id', None)
    return av_session


# TODO: напоминание и ссылка на meet
async def add_new_session(telegram_id: int = None,
                          service_id: UUID = None,
                          av_session_id: UUID = None,
                          is_confirmed: bool = False) -> UUID:
    conn = await get_connection()
    row = await conn.fetchrow("""
    insert into sessions (bot_user_id, service_id, available_session_id, is_confirmed) 
    values ($1, $2, $3, $4)
    returning id
    """, telegram_id, service_id, av_session_id, is_confirmed)
    return row['id']


async def get_user_by_id(telegram_id: int) -> Optional[BotUser]:
    conn = await get_connection()
    row = await conn.fetchrow("""
    select * from bot_users where telegram_id = $1
    """, telegram_id)
    return BotUser(**row) if row else None


async def get_service_by_id(service_id: UUID) -> Service:
    conn = await get_connection()
    row = await conn.fetchrow("""
    select id, name, cost, duration, is_for_benefits from services where id = $1
    """, service_id)
    return Service(id=row['id'],
                   name=row['name'],
                   cost=row['cost'],
                   duration=row['duration'],
                   is_for_benefit=row['is_for_benefits'])


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


async def have_sessions(telegram_id) -> bool:
    conn = await get_connection()
    row = await conn.fetchrow('''
    select exists(select *
    from sessions ss
    where ss.bot_user_id = $1)
    ''', telegram_id)
    return row.get('exists', False)


async def get_available_dates() -> Iterable[DateCallbackFactory]:
    conn = await get_connection()
    rows = await conn.fetch('''
    select date from available_sessions
    where (date = current_date + 1 and time_begin > current_time or
          date > current_date + 1 and date <= current_date + 7) and
        id not in (select available_session_id from sessions)
    group by date order by date
    ''')
    return map(lambda row: DateCallbackFactory(date=row.get('date', None).isoformat()), rows)


async def get_available_times_by_date(date: datetime.date) -> Iterable[TimeCallbackFactory]:
    conn = await get_connection()
    rows = await conn.fetch('''
    select id, time_begin from available_sessions
    where date = $1 and
          id not in (select available_session_id from sessions)
    order by time_begin
    ''', date)
    return map(lambda row: TimeCallbackFactory(uuid=row['id'], time=row['time_begin'].strftime('%H.%M')), rows)


async def get_id_of_primary_session_service() -> Optional[UUID]:
    if not getattr(get_id_of_primary_session_service, 'primary_id', None):
        conn = await get_connection()
        row = await conn.fetchrow("""select id from services
        where name = 'Первичная консультация'""")
        get_id_of_primary_session_service.primary_id = row.get('id', None)

    return get_id_of_primary_session_service.primary_id


async def set_name_and_birth_by_id(telegram_id: int, full_name: str, birth_date: datetime.date) -> None:
    conn = await get_connection()
    await conn.execute('''
    update bot_users
    set full_name = $1, birth_date = $2
    where telegram_id = $3
    ''', full_name, birth_date, telegram_id)


async def get_services_by_benefits(is_for_benefits: bool) -> Iterable[Service]:
    conn = await get_connection()
    rows = await conn.fetch("""
    select id, name, cost, duration from services
    where cost > 0 and is_for_benefits = $1 and is_deleted = false
    order by name
    """, is_for_benefits)
    return map(lambda row: Service(id=row['id'],
                                   name=row['name'],
                                   cost=row['cost'],
                                   duration=row['duration'],
                                   is_for_benefit=is_for_benefits), rows)


async def get_users_nearest_session(telegram_id: int) -> Optional[SessionView]:
    conn = await get_connection()
    row = await conn.fetchrow("""
    select ss.id as id,
           s.name as name,
           av_s.date as date,
           av_s.time_begin as time,
           ss.is_confirmed as is_confirmed,
           s.duration as duration
    from sessions ss
    join available_sessions av_s on av_s.id = ss.available_session_id
    join services s on s.id = ss.service_id
    where (av_s.date = current_date and av_s.time_begin > current_time
    or av_s.date > current_date)
    and ss.bot_user_id = $1
    """, telegram_id)
    return SessionView(**row) if row else None


async def delete_session_by_id(session_id: UUID) -> None:
    conn = await get_connection()
    await conn.execute("""
    delete from sessions
    where id = $1
    """, session_id)


async def update_av_session_by_id(session_id: UUID, av_id: UUID) -> None:
    conn = await get_connection()
    await conn.execute("""
    update sessions
set available_session_id = $1
where id = $2
    """, av_id, session_id)


async def get_all_services() -> Iterable[Service]:
    conn = await get_connection()
    rows = await conn.fetch("""
    select id, name, cost, duration, is_for_benefits from services
    where cost > 0 and is_deleted = false order by name;
    """)
    return map(lambda row: Service(id=row.get('id'),
                                   name=row.get('name'),
                                   cost=row.get('cost'),
                                   duration=row.get('duration'),
                                   is_for_benefit=row.get('is_for_benefit')), rows)


async def delete_service_by_id(service_id: UUID) -> None:
    conn = await get_connection()
    await conn.execute("""
    update services
    set is_deleted = True
    where id = $1
    """, service_id)


async def update_service_filed(service_id: UUID, field: str, value: str | int | bool) -> None:
    conn = await get_connection()
    await conn.execute(f"""
    update services
    set {field} = $1
    where id = $2
    """, value, service_id)

