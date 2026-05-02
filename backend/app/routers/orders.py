from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.deps import get_current_user, require_admin
from ..schemas.order import OrderCreate, OrderUpdate, OrderResponse
from ..models.order import Order, OrderStatus
from ..models.membership_package import MembershipPackage
from ..models.user import User, UserRole

router = APIRouter(prefix="/orders", tags=["Orders"])


def _order_response(order: Order) -> OrderResponse:
    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        package_id=order.package_id,
        total_amount=order.total_amount,
        status=order.status.value,
        start_date=order.start_date,
        end_date=order.end_date,
        created_at=order.created_at,
    )


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    body: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    package = db.query(MembershipPackage).filter(MembershipPackage.id == body.package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Không tìm thấy gói")
    order = Order(
        user_id=current_user.id,
        package_id=package.id,
        total_amount=package.price,
        status=OrderStatus.PENDING,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return _order_response(order)


@router.get("/", response_model=List[OrderResponse])
def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return [_order_response(o) for o in orders]


@router.get("/all", response_model=List[OrderResponse])
def list_all_orders(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    orders = db.query(Order).all()
    return [_order_response(o) for o in orders]


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    if order.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Không có quyền xem đơn này")
    return _order_response(order)


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    body: OrderUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    data = body.model_dump(exclude_unset=True)
    if "status" in data and data["status"] is not None:
        try:
            order.status = OrderStatus(data["status"])
        except ValueError:
            raise HTTPException(status_code=400, detail="Trạng thái không hợp lệ")
        del data["status"]
    for key, value in data.items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return _order_response(order)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    db.delete(order)
    db.commit()
    return None
