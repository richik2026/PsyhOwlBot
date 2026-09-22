from pydantic import BaseModel


class MemorySummaryCreate(BaseModel):
    user_id: int
    topic: str
    summary: str
    emotion: str | None = None
