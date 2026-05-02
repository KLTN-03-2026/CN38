from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..core.database import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    package_id = Column(Integer, ForeignKey("membership_packages.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="orders")
    package = relationship("MembershipPackage", back_populates="orders")
    payment = relationship(
        "Payment",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Order {self.id} - {self.status.value}>"
