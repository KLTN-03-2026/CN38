from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..core.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MEMBER = "member"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.MEMBER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    chat_logs = relationship("AIChatLog", back_populates="user", cascade="all, delete-orphan")
    workout_sessions = relationship("WorkoutSession", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email} - {self.role.value}>"
