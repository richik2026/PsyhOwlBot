import os

import httpx


REALTIME_URL = "https://api.openai.com/v1/realtime/sessions"


async def create_realtime_session(instructions: str):
    """Create an OpenAI Realtime session for Sovenok voice conversations."""

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY missing")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            REALTIME_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": os.getenv("REALTIME_MODEL", "gpt-realtime"),
                "voice": os.getenv("SOVENOK_VOICE", "alloy"),
                "instructions": instructions,
            },
        )

    response.raise_for_status()
    return response.json()
