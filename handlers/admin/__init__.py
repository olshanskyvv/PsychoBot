from aiogram import Router
from aiogram import F

from handlers.admin import services, sessions, timetable
from config import ADMIN_ID, OWNER_ID

router = Router()

router.message.filter(F.from_user.id == OWNER_ID)
router.message.filter(F.from_user.id == ADMIN_ID)
router.callback_query.filter(F.from_user.id == OWNER_ID)
router.callback_query.filter(F.from_user.id == ADMIN_ID)

router.include_router(sessions.router)
router.include_router(services.router)
router.include_router(timetable.router)
