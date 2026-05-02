from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


class AnalyzeWorkoutRequest(BaseModel):
    duration_minutes: float = 0
    calories_burned: float = 0
    intensity_score: float = 0
    sessions_last_week: float = 0


class AnalyzeWorkoutResponse(BaseModel):
    label: str
    probability: float
    hint: str


class AIChatLogCreate(BaseModel):
    message: str
    response: Optional[str] = None


class AIChatLogUpdate(BaseModel):
    message: Optional[str] = None
    response: Optional[str] = None


class AIChatLogResponse(BaseModel):
    id: int
    user_id: int
    message: str
    response: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
