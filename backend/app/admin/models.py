from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.base import Base


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)

    telegram_id = Column(Integer, unique=True, nullable=False)
    role = Column(String, default="admin")

    created_at = Column(DateTime, default=datetime.utcnow)
