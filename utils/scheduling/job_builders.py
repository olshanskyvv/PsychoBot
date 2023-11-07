import datetime
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db.models import UUID, AvailableSession
from db.driver import (
    get_available_sessions_by_id,
    get_session_by_id,
    delete_session_by_id
)

from utils import bot


async def get_datetime(av_session_id: UUID) -> datetime.datetime:
    av_session = await get_available_sessions_by_id(av_session_id)
    date = av_session.date
    time = av_session.time_begin
    time_point = datetime.datetime(year=date.year,
                                   month=date.month,
                                   day=date.day,
                                   hour=time.hour,
                                   minute=time.minute)
    return time_point


async def get_confirm_check_time(av_session_id: UUID) -> datetime.datetime:
    time_point = await get_datetime(av_session_id)
    check_time = time_point - datetime.timedelta(days=1)
    # check_time = datetime.datetime.now() + datetime.timedelta(seconds=40)
    logging.info(check_time)
    return check_time


async def get_alert_time(av_session_id: UUID) -> datetime.datetime:
    time_point = await get_datetime(av_session_id)
    check_time = time_point - datetime.timedelta(hours=1)
    # check_time = datetime.datetime.now() + datetime.timedelta(seconds=30)
    logging.info(check_time)
    return check_time


async def session_alert_job(session_id: UUID) -> None:
    session = await get_session_by_id(session_id)
    if not session:
        return
    if not session.is_confirmed:
        return
    session_datetime = await get_datetime(session.available_session.id)
    if session_datetime - datetime.datetime.now() > datetime.timedelta(hours=1):
        return
    # TODO: Google Meet
    await bot.send_message(chat_id=session.user.telegram_id,
                           text="Напоминаем, что через час у Вас запланирована сессия")


async def confirm_checking_job(session_id: UUID) -> None:
    logging.info('job starts')
    session = await get_session_by_id(session_id)
    if not session:
        return

    if session.is_confirmed:
        return

    await bot.send_message(chat_id=session.user.telegram_id,
                           text="За сутки до Вашей сессии запись не была подтверждена. "
                                "В связи с этим запись была отменена")
    await delete_session_by_id(session_id)

    # scheduler.add_job(job, 'date', run_date=check_time)
