from typing import Callable, Any, Awaitable

from aiogram.types import CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from aiogram import BaseMiddleware


job_stores = {
    'default': RedisJobStore(host='localhost', port=6379)
}


class ScheduleCallbackMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        self.scheduler = scheduler

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: dict[str, Any]
    ) -> Any:
        data['scheduler'] = self.scheduler
        await handler(event, data)



