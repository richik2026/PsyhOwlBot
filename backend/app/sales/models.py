from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric

from app.database.base import Base


class Sale(Base):
    """Purchase event received from Tribute webhook.

    Stores attribution data for admin rankings and revenue analytics.
    """

    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=True)

    provider = Column(String(50), default="tribute")

    # Unique provider event/payment identifiers prevent duplicate webhook processing.
    provider_event_id = Column(String(255), unique=True, nullable=True)
    provider_payment_id = Column(String(255), unique=True, nullable=True)

    amount = Column(Numeric(10, 2), nullable=True)
    currency = Column(String(10), nullable=True)

    purchased_at = Column(DateTime, default=datetime.utcnow)
