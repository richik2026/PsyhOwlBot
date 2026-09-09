from datetime import datetime

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    telegram_id: int
    username: str | None = None
    first_name: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
