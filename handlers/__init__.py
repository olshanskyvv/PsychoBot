from aiogram import Router
from handlers import recording, agreement, profile, session_view

router = Router()

router.include_router(agreement.router)
router.include_router(profile.router)
router.include_router(recording.router)
router.include_router(session_view.router)
