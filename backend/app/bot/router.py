from aiogram import Router

from app.bot.handlers import start, admin, reels


router = Router()

router.include_router(start.router)
router.include_router(admin.router)
router.include_router(reels.router)
