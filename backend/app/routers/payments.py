from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.deps import get_current_user, require_admin
from ..schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse
from ..models.payment import Payment
from ..models.order import Order
from ..models.user import User, UserRole

router = APIRouter(prefix="/payments", tags=["Payments"])


def _order_for_payment(db: Session, payment: Payment) -> Order:
    order = db.query(Order).filter(Order.id == payment.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    return order


def _ensure_payment_owner_or_admin(db: Session, payment: Payment, user: User) -> None:
    order = _order_for_payment(db, payment)
    if user.role == UserRole.ADMIN:
        return
    if order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Không có quyền")


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(
    body: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == body.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    if order.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Không có quyền")
    existing = db.query(Payment).filter(Payment.order_id == body.order_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Đơn hàng đã có thanh toán")
    payment = Payment(
        order_id=body.order_id,
        amount=body.amount,
        payment_method=body.payment_method,
        transaction_id=body.transaction_id,
        status="pending",
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


@router.get("/", response_model=List[PaymentResponse])
def list_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.ADMIN:
        return db.query(Payment).all()
    return (
        db.query(Payment)
        .join(Order, Payment.order_id == Order.id)
        .filter(Order.user_id == current_user.id)
        .all()
    )


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Không tìm thấy thanh toán")
    _ensure_payment_owner_or_admin(db, payment, current_user)
    return payment


@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(
    payment_id: int,
    body: PaymentUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Không tìm thấy thanh toán")
    data = body.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(payment, key, value)
    db.commit()
    db.refresh(payment)
    return payment


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Không tìm thấy thanh toán")
    db.delete(payment)
    db.commit()
    return None
