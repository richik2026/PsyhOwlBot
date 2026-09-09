from aiogram import Router
from aiogram.types import Update

router = Router()


@router.post('/tribute/webhook')
async def tribute_webhook(payload: dict):
    """
    Tribute payment webhook endpoint.

    Real signature validation and payload mapping are added after
    receiving Tribute webhook format and secret key.
    """
    return {"status": "received"}
