from aiogram import Router
from handlers.recording import choice, primary, secondary

router = Router()

router.include_router(choice.router)
router.include_router(primary.router)
router.include_router(secondary.router)
