import os
import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.miniapp.auth import verify_init_data


router = APIRouter(prefix="/miniapp", tags=["miniapp"])


class MiniAppAuthRequest(BaseModel):
    init_data: str


@router.get("/health")
async def health():
    return {
        "service": "sovenok-miniapp",
        "status": "ok"
    }


@router.post("/auth")
async def auth(payload: MiniAppAuthRequest):
    if not payload.init_data:
        raise HTTPException(status_code=400, detail="init_data required")

    bot_token = os.getenv("BOT_TOKEN")

    if not bot_token:
        raise HTTPException(
            status_code=500,
            detail="BOT_TOKEN not configured"
        )

    if not verify_init_data(
        payload.init_data,
        bot_token
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Telegram initData"
        )

    return {
        "authenticated": True,
        "service": "sovenok-miniapp"
    }
