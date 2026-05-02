from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MembershipPackageBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    duration_days: int
    max_workouts_per_week: Optional[int] = None
    is_active: bool = True


class MembershipPackageCreate(MembershipPackageBase):
    pass


class MembershipPackageUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    duration_days: Optional[int] = None
    max_workouts_per_week: Optional[int] = None
    is_active: Optional[bool] = None


class MembershipPackageResponse(MembershipPackageBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
