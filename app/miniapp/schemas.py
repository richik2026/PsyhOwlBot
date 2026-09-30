from pydantic import BaseModel


class MiniAppAuthResponse(BaseModel):
    user_id: int
    telegram_id: int
    subscription_active: bool = False
    voice_enabled: bool = True
    voice_seconds_left: int = 0
