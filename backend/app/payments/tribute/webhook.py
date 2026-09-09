from fastapi import APIRouter, Request, HTTPException

from app.payments.tribute.validator import validate_tribute_signature

router = APIRouter(prefix="/webhooks/tribute", tags=["tribute"])


@router.post("")
async def tribute_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("trbt-signature")

    if not validate_tribute_signature(payload, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Payment processing will be connected here:
    # 1. identify user
    # 2. identify referral admin
    # 3. create sale
    # 4. activate access

    return {"status": "ok"}
