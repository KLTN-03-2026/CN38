from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderCreate(BaseModel):
    package_id: int


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class OrderResponse(BaseModel):
    id: int
    user_id: int
    package_id: int
    total_amount: float
    status: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
