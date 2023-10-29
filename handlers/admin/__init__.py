from aiogram import Router
from aiogram import F

from handlers.admin import services, sessions, timetable
from config import ADMIN_ID, OWNER_ID
from utils.filters import UsersFilter

router = Router()

router.message.filter(UsersFilter(ADMIN_ID, OWNER_ID))

router.include_router(sessions.router)
router.include_router(services.router)
router.include_router(timetable.router)
