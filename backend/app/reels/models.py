from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class AdminReels(Base):
    __tablename__ = "admin_reels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    admin_id: Mapped[int] = mapped_column(
        ForeignKey("admins.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    number_of_reels: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
