from pydantic import BaseModel
from typing import Optional


class TributePaymentEvent(BaseModel):
    event_type: str
    user_id: Optional[int] = None
    payment_id: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
