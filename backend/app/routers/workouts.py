from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from ..core.database import get_db
from ..core.deps import get_current_user, require_admin
from ..schemas.workout_session import WorkoutSessionCreate, WorkoutSessionUpdate, WorkoutSessionResponse
from ..models.workout_session import WorkoutSession
from ..models.user import User, UserRole

router = APIRouter(prefix="/workouts", tags=["Workout Sessions"])


def _session_owner_or_admin(session: WorkoutSession, user: User) -> None:
    if user.role == UserRole.ADMIN:
        return
    if session.user_id != user.id:
        raise HTTPException(status_code=403, detail="Không có quyền")


@router.post("/", response_model=WorkoutSessionResponse, status_code=status.HTTP_201_CREATED)
def create_workout(
    body: WorkoutSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = WorkoutSession(user_id=current_user.id, **body.model_dump())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.get("/", response_model=List[WorkoutSessionResponse])
def list_my_workouts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(WorkoutSession).filter(WorkoutSession.user_id == current_user.id).all()


@router.get("/all", response_model=List[WorkoutSessionResponse])
def list_all_workouts(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return db.query(WorkoutSession).all()


@router.get("/{session_id}", response_model=WorkoutSessionResponse)
def get_workout(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = db.query(WorkoutSession).filter(WorkoutSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Không tìm thấy buổi tập")
    _session_owner_or_admin(session, current_user)
    return session


@router.put("/{session_id}", response_model=WorkoutSessionResponse)
def update_workout(
    session_id: int,
    body: WorkoutSessionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = db.query(WorkoutSession).filter(WorkoutSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Không tìm thấy buổi tập")
    _session_owner_or_admin(session, current_user)
    data = body.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(session, key, value)
    db.commit()
    db.refresh(session)
    return session


@router.patch("/{session_id}/finish", response_model=WorkoutSessionResponse)
def finish_workout(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = db.query(WorkoutSession).filter(WorkoutSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Không tìm thấy buổi tập")
    _session_owner_or_admin(session, current_user)
    session.ended_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(session)
    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = db.query(WorkoutSession).filter(WorkoutSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Không tìm thấy buổi tập")
    _session_owner_or_admin(session, current_user)
    db.delete(session)
    db.commit()
    return None
