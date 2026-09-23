import hashlib
import hmac
import os

from fastapi import APIRouter, Request, HTTPException

from app.database.session import AsyncSessionLocal
from app.tribute.service import process_tribute_payment

router = APIRouter(prefix="/tribute", tags=["tribute"])


@router.post("/webhook")
async def webhook(request: Request):
    body = await request.body()

    secret = os.getenv("TRIBUTE_WEBHOOK_SECRET")
    signature = request.headers.get("trbt-signature")

    if secret and signature:
        expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, signature):
            raise HTTPException(status_code=403, detail="Invalid signature")

    payload = await request.json()

    user_id = payload.get("user_id") or payload.get("telegram_id")
    payment_id = payload.get("id") or payload.get("payment_id")
    amount = payload.get("amount")
    currency = payload.get("currency", "RUB")

    if not user_id or not payment_id or amount is None:
        raise HTTPException(status_code=400, detail="Invalid payload")

    async with AsyncSessionLocal() as session:
        await process_tribute_payment(
            session=session,
            user_id=int(user_id),
            amount=float(amount),
            payment_id=str(payment_id),
            currency=currency,
        )

    return {"status": "ok"}
