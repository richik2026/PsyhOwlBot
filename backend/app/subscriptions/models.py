from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.database.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Payment provider. Current provider is Tribute.
    provider = Column(String(50), default="tribute")

    # Payment identifier received from Tribute.
    tribute_payment_id = Column(
        String(255),
        unique=True,
        nullable=True,
    )

    status = Column(String, default="active")

    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)

    # Product rules: 30 days access, 60 hours total.
    hours_total = Column(Integer, default=60)
    hours_used = Column(Integer, default=0)
