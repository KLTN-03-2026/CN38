from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Any
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1)
    phone: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    phone: Optional[str]
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

    @field_validator("role", mode="before")
    @classmethod
    def role_to_str(cls, v: Any) -> str:
        if hasattr(v, "value"):
            return str(v.value)
        return str(v)


class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
