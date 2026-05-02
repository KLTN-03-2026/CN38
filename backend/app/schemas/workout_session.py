from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WorkoutSessionCreate(BaseModel):
    title: Optional[str] = None
    duration_minutes: Optional[int] = None
    calories_burned: Optional[float] = None
    intensity_score: Optional[float] = None
    notes: Optional[str] = None


class WorkoutSessionUpdate(BaseModel):
    title: Optional[str] = None
    duration_minutes: Optional[int] = None
    calories_burned: Optional[float] = None
    intensity_score: Optional[float] = None
    notes: Optional[str] = None
    ended_at: Optional[datetime] = None


class WorkoutSessionResponse(BaseModel):
    id: int
    user_id: int
    title: Optional[str] = None
    duration_minutes: Optional[int] = None
    calories_burned: Optional[float] = None
    intensity_score: Optional[float] = None
    notes: Optional[str] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
