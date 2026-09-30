from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

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

    return {
        "authenticated": True,
        "message": "Mini App auth endpoint ready"
    }
