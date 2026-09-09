from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime

from app.database.base import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    summary = Column(Text, nullable=True)
    topics = Column(Text, nullable=True)
    emotion = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
