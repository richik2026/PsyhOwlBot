from aiogram import Router

from app.bot.handlers import start, admin, reels, dashboard, ratings, subscription


router = Router()

router.include_router(start.router)
router.include_router(admin.router)
router.include_router(reels.router)
router.include_router(dashboard.router)
router.include_router(ratings.router)
router.include_router(subscription.router)
