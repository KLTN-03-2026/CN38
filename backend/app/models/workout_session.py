from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    calories_burned = Column(Float, nullable=True)
    intensity_score = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="workout_sessions")

    def __repr__(self):
        return f"<WorkoutSession {self.id} user={self.user_id}>"
