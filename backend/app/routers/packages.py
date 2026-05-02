from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.deps import require_admin
from ..schemas.membership_package import (
    MembershipPackageCreate,
    MembershipPackageResponse,
    MembershipPackageUpdate,
)
from ..models.membership_package import MembershipPackage
from ..models.user import User

router = APIRouter(prefix="/packages", tags=["Membership Packages"])


@router.post("/", response_model=MembershipPackageResponse, status_code=status.HTTP_201_CREATED)
def create_package(
    package: MembershipPackageCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    db_package = MembershipPackage(**package.model_dump())
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    return db_package


@router.get("/", response_model=List[MembershipPackageResponse])
def get_all_packages(db: Session = Depends(get_db)):
    return db.query(MembershipPackage).all()


@router.get("/{package_id}", response_model=MembershipPackageResponse)
def get_package(package_id: int, db: Session = Depends(get_db)):
    package = db.query(MembershipPackage).filter(MembershipPackage.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Không tìm thấy gói")
    return package


@router.put("/{package_id}", response_model=MembershipPackageResponse)
def update_package(
    package_id: int,
    body: MembershipPackageUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    package = db.query(MembershipPackage).filter(MembershipPackage.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Không tìm thấy gói")
    data = body.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(package, key, value)
    db.commit()
    db.refresh(package)
    return package


@router.delete("/{package_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_package(
    package_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    package = db.query(MembershipPackage).filter(MembershipPackage.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Không tìm thấy gói")
    db.delete(package)
    db.commit()
    return None
