import os

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.voice.prompt import SOVENOK_PROMPT

router = APIRouter(prefix="/voice", tags=["voice"])


class RealtimeSessionRequest(BaseModel):
    user_id: int | None = None


@router.post("/realtime/session")
async def create_realtime_session(payload: RealtimeSessionRequest):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise HTTPException(500, "OPENAI_API_KEY missing")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/realtime/sessions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": os.getenv("REALTIME_MODEL", "gpt-realtime"),
                "voice": os.getenv("SOVENOK_VOICE", "alloy"),
                "instructions": SOVENOK_PROMPT,
            },
        )

    if response.status_code != 200:
        raise HTTPException(response.status_code, response.text)

    return response.json()
