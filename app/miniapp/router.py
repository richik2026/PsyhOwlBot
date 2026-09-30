from fastapi import APIRouter

router = APIRouter(prefix="/miniapp", tags=["miniapp"])


@router.get("/health")
async def health():
    return {
        "service": "sovenok-miniapp",
        "status": "ok"
    }
