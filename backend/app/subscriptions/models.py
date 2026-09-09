from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    active_until: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total_seconds: Mapped[int] = mapped_column(Integer, default=216000, nullable=False)
    used_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    daily_limit_seconds: Mapped[int] = mapped_column(Integer, default=7200, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
