from fastapi import APIRouter, Request

from app.tribute.service import process_tribute_payment

router = APIRouter(prefix="/tribute", tags=["tribute"])


@router.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()

    # Payload mapping depends on Tribute webhook specification.
    # Keep endpoint ready for signature validation and mapping.
    return {"status": "received"}
