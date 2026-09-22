from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class MemoryRecord:
    """Short-term structure for Krish user memories.

    Audio is intentionally not stored. Only structured summaries and
    important context should be persisted.
    """

    user_id: int
    topic: str
    summary: str
    emotion: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)


class MemoryService:
    """Interface for future AI-generated conversation memory."""

    async def create_summary(
        self,
        user_id: int,
        topic: str,
        summary: str,
        emotion: str | None = None,
    ) -> MemoryRecord:
        return MemoryRecord(
            user_id=user_id,
            topic=topic,
            summary=summary,
            emotion=emotion,
        )
