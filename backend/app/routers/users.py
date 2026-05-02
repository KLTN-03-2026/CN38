from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.deps import get_current_user, require_admin
from ..schemas.user import UserResponse, UserUpdate, UserPasswordUpdate
from ..models.user import User, UserRole
from ..services.auth_service import AuthService

router = APIRouter(prefix="/users", tags=["Users"])
auth_service = AuthService()


@router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


@router.get("/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    users = db.query(User).all()
    return [UserResponse.model_validate(u) for u in users]


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    return UserResponse.model_validate(user)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    body: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    data = body.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


@router.patch("/me/password", response_model=UserResponse)
def change_my_password(
    body: UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not auth_service.verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Mật khẩu hiện tại không đúng")
    current_user.hashed_password = auth_service.hash_password(body.new_password)
    db.commit()
    db.refresh(current_user)
    return UserResponse.model_validate(current_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Không thể xóa chính mình")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    db.delete(user)
    db.commit()
    return None
