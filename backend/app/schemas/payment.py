from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None


class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    status: Optional[str] = None
    paid_at: Optional[datetime] = None


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    status: str
    paid_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
